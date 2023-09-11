import abc
import datetime
import json
from typing import Any, Dict


class BaseStorage(abc.ABC):
    """Абстрактное хранилище состояния.

    Позволяет сохранять и получать состояние.
    Способ хранения состояния может варьироваться в зависимости
    от итоговой реализации. Например, можно хранить информацию
    в базе данных или в распределённом файловом хранилище.
    """

    @abc.abstractmethod
    def save_state(self, state: Dict[str, Any]) -> None:
        """Сохранить состояние в хранилище."""
        pass

    @abc.abstractmethod
    def retrieve_state(self) -> Dict[str, Any]:
        """Получить состояние из хранилища."""
        pass


class JsonFileStorage(BaseStorage):
    """Реализация хранилища, использующего локальный файл.
    Формат хранения: JSON
    """

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def save_state(self, state: Dict[str, Any]) -> None:
        """Сохранить состояние в хранилище."""
        with open(self.file_path, 'w') as outfile:
            json.dump(state, outfile)

    def retrieve_state(self) -> Dict[str, Any]:
        """Получить состояние из хранилища."""
        dict = {
            'person': datetime.datetime(1, 1, 1).isoformat(),
            'genre': datetime.datetime(1, 1, 1).isoformat(),
            'film_work': datetime.datetime(1, 1, 1).isoformat(),
        }
        try:
            with open(self.file_path) as outfile:
                return json.load(outfile)
        except FileNotFoundError:
            with open(self.file_path, 'a') as outfile:
                json.dump(dict, outfile)
            return dict


class State:
    """Класс для работы с состояниями."""

    def __init__(self, storage: JsonFileStorage) -> None:
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        """Установить состояние для определённого ключа."""
        states = self.storage.retrieve_state()
        states[key] = value
        self.storage.save_state(states)

    def get_state(self, key: str) -> Any:
        """Получить состояние по определённому ключу."""
        state = self.storage.retrieve_state()
        value = state.get(key)
        return value
