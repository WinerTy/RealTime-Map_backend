from pathlib import Path

from starlette.templating import Jinja2Templates

from core.config import conf


class TemplateManager:
    def __init__(self, path: Path):
        self._engine = Jinja2Templates(directory=path)
        self._add_filters()
        self._add_globals()

    @property
    def engine(self) -> Jinja2Templates:
        """
        Прямой доступ к экземпляру
        :return:
        """
        return self._engine

    def _add_filters(self) -> None:
        """
        Метод для добавления кастомных фильтров для шаблонизатора
        :return:
        """
        pass

    def _add_globals(self) -> None:
        """
        Метод для добавления глобальных значений
        :return:
        """
        self.engine.env.globals["base_url"] = conf.frontend.url
