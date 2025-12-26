from .base_generator import BaseGenerator
from .generator_factory import factory, GeneratorFactory
from .user_generator import UserGenerator
from .vulnerability_generator import VulnerabilityGenerator
from .sensitive_generator import SensitiveDataGenerator
from .penetration_generator import PenetrationGenerator

# Регистрируем генераторы
factory.register_generator("user", UserGenerator)
factory.register_generator("vulnerability", VulnerabilityGenerator)
factory.register_generator("sensitive_data", SensitiveDataGenerator)
factory.register_generator("penetration", PenetrationGenerator)

__all__ = [
    'BaseGenerator',
    'GeneratorFactory',
    'factory',
    'UserGenerator',
    'VulnerabilityGenerator',
    'SensitiveDataGenerator',
    'PenetrationGenerator'
]