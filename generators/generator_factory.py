from typing import Dict, Type, Optional, List
from .base_generator import BaseGenerator
import logging


class GeneratorFactory:
    """
    Фабрика для создания и управления генераторами данных.
    """

    def __init__(self):
        self._generators: Dict[str, Type[BaseGenerator]] = {}
        self.logger = logging.getLogger(__name__)

    def register_generator(self, generator_type: str, generator_class: Type[BaseGenerator]) -> None:
        """
        Регистрирует генератор в фабрике.

        Args:
            generator_type (str): Тип генератора
            generator_class (Type[BaseGenerator]): Класс генератора
        """
        self._generators[generator_type] = generator_class
        self.logger.info(f"Зарегистрирован генератор: {generator_type}")

    def create_generator(self, generator_type: str, **kwargs) -> Optional[BaseGenerator]:
        """
        Создает экземпляр генератора по типу.

        Args:
            generator_type (str): Тип генератора
            **kwargs: Дополнительные параметры для конструктора генератора

        Returns:
            Optional[BaseGenerator]: Экземпляр генератора или None если тип не найден
        """
        if generator_type not in self._generators:
            self.logger.error(f"Генератор типа '{generator_type}' не найден")
            return None

        try:
            generator_class = self._generators[generator_type]
            return generator_class(**kwargs)
        except Exception as e:
            self.logger.error(f"Ошибка при создании генератора {generator_type}: {e}")
            return None

    def get_available_generators(self) -> List[str]:
        """
        Возвращает список доступных типов генераторов.

        Returns:
            List[str]: Список типов генераторов
        """
        return list(self._generators.keys())

    def is_generator_available(self, generator_type: str) -> bool:
        """
        Проверяет, доступен ли генератор указанного типа.

        Args:
            generator_type (str): Тип генератора для проверки

        Returns:
            bool: True если генератор доступен, False в противном случае
        """
        return generator_type in self._generators


# Создаем глобальный экземпляр фабрики
factory = GeneratorFactory()