from .base_generator import BaseGenerator
from .generator_factory import factory, GeneratorFactory
from .user_generator import UserGenerator

# Регистрируем генераторы
factory.register_generator("user", UserGenerator)

__all__ = [
    'BaseGenerator',
    'GeneratorFactory',
    'factory',
    'UserGenerator'
]