from pathlib import Path

from starlette.templating import Jinja2Templates


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
        pass
