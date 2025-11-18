from .base_generator import BaseGenerator
from .generator_factory import factory, GeneratorFactory
from .user_generator import UserGenerator
from .vulnerability_generator import VulnerabilityGenerator

# Регистрируем генераторы
factory.register_generator("user", UserGenerator)
factory.register_generator("vulnerability", VulnerabilityGenerator)

__all__ = [
    'BaseGenerator',
    'GeneratorFactory',
    'factory',
    'UserGenerator',
    'VulnerabilityGenerator'
]