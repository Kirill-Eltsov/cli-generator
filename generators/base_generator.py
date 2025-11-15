from abc import ABC, abstractmethod
from typing import Dict, Any, List
import logging


class BaseGenerator(ABC):
    """
    Абстрактный базовый класс для всех генераторов данных.
    Определяет общий интерфейс для генерации тестовых данных.
    """

    def __init__(self, locale: str = "ru_RU"):
        self.locale = locale
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def generate_row(self) -> Dict[str, Any]:
        """
        Генерирует одну строку данных.

        Returns:
            Dict[str, Any]: Словарь с данными, где ключ - название поля, значение - сгенерированные данные
        """
        pass

    @abstractmethod
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """
        Валидирует сгенерированные данные.

        Args:
            data (Dict[str, Any]): Данные для валидации

        Returns:
            bool: True если данные валидны, False в противном случае
        """
        pass

    def generate_batch(self, count: int) -> List[Dict[str, Any]]:
        """
        Генерирует несколько строк данных.

        Args:
            count (int): Количество строк для генерации

        Returns:
            List[Dict[str, Any]]: Список сгенерированных строк
        """
        batch = []
        for i in range(count):
            try:
                row = self.generate_row()
                if self.validate_data(row):
                    batch.append(row)
                else:
                    self.logger.warning(f"Пропущена невалидная строка: {row}")
            except Exception as e:
                self.logger.error(f"Ошибка при генерации строки {i}: {e}")
        return batch

    @property
    @abstractmethod
    def generator_type(self) -> str:
        """
        Возвращает тип генератора.

        Returns:
            str: Тип генератора (например, 'user', 'payment', 'security')
        """
        pass