from faker import Faker
from typing import Dict, Any
from .base_generator import BaseGenerator


class UserGenerator(BaseGenerator):
    """
    Генератор тестовых данных пользователей.
    """

    def __init__(self, locale: str = "ru_RU"):
        super().__init__(locale)
        self.fake = Faker(locale)

    def generate_row(self) -> Dict[str, Any]:
        """
        Генерирует данные одного пользователя.
        """
        return {
            "id": self.fake.uuid4(),
            "username": self.fake.user_name(),
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "email": self.fake.email(),
            "phone": self.fake.phone_number(),
            "address": self.fake.address().replace('\n', ', '),
            "birth_date": self.fake.date_of_birth(minimum_age=18, maximum_age=65).isoformat()
        }

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """
        Проверяет валидность данных пользователя.
        """
        required_fields = ['id', 'username', 'email']

        # Проверяем наличие обязательных полей
        for field in required_fields:
            if field not in data or not data[field]:
                return False

        # Проверяем формат email
        if '@' not in data['email']:
            return False

        return True

    @property
    def generator_type(self) -> str:
        return "user"