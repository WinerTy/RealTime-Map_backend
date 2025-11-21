import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from modules.gamefication.repository import NewLevelRepository
from .fixtures import test_level, test_levels


class TestLevelRepository:
    """Тесты для NewLevelRepository (LevelRepository)"""

    @pytest.mark.asyncio
    async def test_get_by_id(self, db_session: AsyncSession, test_level):
        """Тест получения уровня по ID"""
        repo = NewLevelRepository(session=db_session)

        level = await repo.get_by_id(test_level.id)

        assert level is not None
        assert level.id == test_level.id
        assert level.level == test_level.level
        assert level.required_exp == test_level.required_exp

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, db_session: AsyncSession):
        """Тест получения несуществующего уровня"""
        repo = NewLevelRepository(session=db_session)

        level = await repo.get_by_id(99999)

        assert level is None

    @pytest.mark.asyncio
    async def test_get_levels_count(self, db_session: AsyncSession, test_levels):
        """Тест проверки количества созданных уровней"""
        repo = NewLevelRepository(session=db_session)

        # Проверяем что все уровни созданы
        max_level = await repo.get_max_level()
        assert max_level is not None
        assert max_level.level == 6

    @pytest.mark.asyncio
    async def test_get_next_level(self, db_session: AsyncSession, test_levels):
        """Тест получения следующего уровня"""
        repo = NewLevelRepository(session=db_session)

        next_level = await repo.get_next_level(current_level=1)

        assert next_level is not None
        assert next_level.level == 2
        assert next_level.is_active is True

    @pytest.mark.asyncio
    async def test_get_next_level_from_middle(
        self, db_session: AsyncSession, test_levels
    ):
        """Тест получения следующего уровня из середины"""
        repo = NewLevelRepository(session=db_session)

        # Получаем уровень 4 (следующий после 3)
        next_level = await repo.get_next_level(current_level=3)

        assert next_level is not None
        assert next_level.level == 4
        assert next_level.required_exp == 500

    @pytest.mark.asyncio
    async def test_get_next_level_inactive_skipped(
        self, db_session: AsyncSession, test_levels
    ):
        """Тест что неактивный уровень не возвращается"""
        repo = NewLevelRepository(session=db_session)

        # Уровень 6 неактивен поэтому результат None
        next_level = await repo.get_next_level(current_level=5)

        assert next_level is None

    @pytest.mark.asyncio
    async def test_get_next_level_last_level(
        self, db_session: AsyncSession, test_levels
    ):
        """Тест получения следующего уровня когда достигнут максимум"""
        repo = NewLevelRepository(session=db_session)

        # Вариант для того что уровень был переведен в инактив а следуйщего нету
        next_level = await repo.get_next_level(current_level=6)

        assert next_level is None

    @pytest.mark.asyncio
    async def test_get_next_level_non_existent(
        self, db_session: AsyncSession, test_levels
    ):
        """Тест получения следующего уровня для несуществующего текущего уровня"""
        repo = NewLevelRepository(session=db_session)

        next_level = await repo.get_next_level(current_level=99)

        assert next_level is None

    @pytest.mark.asyncio
    async def test_get_max_level(self, db_session: AsyncSession, test_levels):
        """Тест получения максимального уровня"""
        repo = NewLevelRepository(session=db_session)

        max_level = await repo.get_max_level()

        assert max_level is not None
        assert max_level.level == 6
        assert max_level.required_exp == 2000

    @pytest.mark.asyncio
    async def test_get_max_level_empty(self, db_session: AsyncSession, test_levels):
        """Тест получения максимального уровня когда уровней нет"""
        repo = NewLevelRepository(session=db_session)

        max_level = await repo.get_max_level()

        assert max_level is None

    @pytest.mark.asyncio
    async def test_get_max_level_single(self, db_session: AsyncSession, test_level):
        """Тест получения максимального уровня когда есть только один уровень"""
        repo = NewLevelRepository(session=db_session)

        max_level = await repo.get_max_level()

        assert max_level is not None
        assert max_level.id == test_level.id
        assert max_level.level == 1

    @pytest.mark.asyncio
    async def test_delete_level(self, db_session: AsyncSession, test_level):
        """Тест удаления уровня"""
        repo = NewLevelRepository(session=db_session)

        result = await repo.delete(test_level.id)

        assert result is not None
        assert result.id == test_level.id

        deleted_level = await repo.get_by_id(test_level.id)
        assert deleted_level is None

    @pytest.mark.asyncio
    async def test_levels_ordered_by_level_number(
        self, db_session: AsyncSession, test_levels
    ):
        """Тест что уровни правильно упорядочены по возрастанию"""
        repo = NewLevelRepository(session=db_session)

        # Проверяем последовательно что уровни идут по возрастанию
        level_1 = await repo.get_by_id(test_levels[0].id)
        level_2 = await repo.get_by_id(test_levels[1].id)
        assert level_1.required_exp < level_2.required_exp

    @pytest.mark.asyncio
    async def test_get_next_level_progression(
        self, db_session: AsyncSession, test_levels
    ):
        """Тест последовательного получения следующих уровней"""
        repo = NewLevelRepository(session=db_session)

        current_level = 1
        expected_levels = [2, 3, 4, 5]

        for expected_level_num in expected_levels:
            next_level = await repo.get_next_level(current_level)
            assert next_level is not None
            assert next_level.level == expected_level_num
            current_level = next_level.level
