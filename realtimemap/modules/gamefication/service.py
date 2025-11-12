import logging
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from modules.user.repository import UserRepository
from modules.user_subscription.repository import UserSubscriptionRepository
from .schemas import CreateUserExpHistory
from .. import ExpAction
from ..user.schemas import UserUpdate

if TYPE_CHECKING:
    from .repository import (
        UserExpHistoryRepository,
        ExpActionRepository,
        LevelRepository,
    )
    from modules import User

logger = logging.getLogger(__name__)


class GameFicationService:
    def __init__(
        self,
        history_repo: "UserExpHistoryRepository",
        action_repo: "ExpActionRepository",
        level_repo: "LevelRepository",
        user_repo: "UserRepository",
        user_subs_repo: "UserSubscriptionRepository",
    ):
        self.user_repo = user_repo
        self.history_repo = history_repo
        self.action_repo = action_repo
        self.level_repo = level_repo
        self.user_subs_repo = user_subs_repo

    async def great_user_exp(self, user: "User", action_type: str) -> None:
        try:
            # Получение конфига из бд
            action = await self._get_action(action_type)
            if not action:
                logger.info("Not found active action")
                return

            if not action.is_repeatable:
                # Проверка начисления опыта за не повторяющиеся действия
                existing = await self._check_if_already_granted(user.id, action.id)
                if existing:
                    logger.info(
                        f"User {user.id} has already granted exp for {action.id}"
                    )
                    return

            # Проверка дневных лимитов начисления
            if not await self._check_daily_limits(
                user.id, action.id, action.max_per_day
            ):
                logger.info(f"User {user.id} great daily limits for action {action.id}")
                return

            user_sub = await self.user_subs_repo.get_active_subscriptions(
                user.id
            )  # получить подписку пользователя и учитывать ее бонусы

            base_exp = action.base_exp
            final_exp = base_exp
            level_before = user.level
            multiplier = Decimal(1.0)

            if user_sub:
                sub_bonuses = user_sub.plan.features
                if "exp_multiplier" in sub_bonuses:
                    multiplier: Decimal = sub_bonuses["exp_multiplier"]
                    final_exp = int(base_exp * multiplier)
                    print("Опыт с учетом множителя ", final_exp)

            upd_exp = UserUpdate(
                total_exp=user.total_exp + final_exp, curent_exp=user.current_exp
            )
            await self.user_repo.update_user(user, upd_exp)
            level_after = await self.user_repo.level_up(user.id)
            history_data = CreateUserExpHistory(
                user_id=user.id,
                action_id=action.id,
                base_exp=base_exp,
                total_exp=final_exp,
                exp_before=user.current_exp,
                level_before=level_before,
                subscription_plan_id=user_sub.plan_id if user_sub else None,
                is_revoked=False,
                multiplier=multiplier,
                source_type=None,
                source_id=None,
                level_after=level_after,
            )
            await self._create_history(history_data)
        except Exception as e:
            logger.error("GameFicationService.great_user_exp", e)
            pass

    async def _create_history(self, data: CreateUserExpHistory):
        history = await self.history_repo.create(data)
        return history

    async def _get_action(self, action_type: str) -> Optional[ExpAction]:
        action = await self.action_repo.get_action_by_type(action_type)
        return action

    async def _check_if_already_granted(self, user_id: int, action_id: int) -> bool:
        result = await self.history_repo.check_if_user_alredy_granted(
            user_id, action_id
        )
        return result

    async def _check_daily_limits(
        self, user_id: int, action_id: int, daily_limits: int
    ) -> bool:
        """
        Проверка на дневные лимиты начисления опыта. Возвращает Fasle если дневные лимиты на данное событие превышены
        :param user.id:
        :param action_id:
        :param daily_limits:
        :return:
        """
        try:
            user_limits = await self.history_repo.get_user_daily_limit_by_action(
                user_id, action_id
            )
            if user_limits >= daily_limits:
                return False
            return True
        except Exception as e:
            logger.error("GameFicationService.checking_daily_limits", e)
            return False
