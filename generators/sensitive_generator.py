from faker import Faker
from typing import Dict, Any, List
import random
from .base_generator import BaseGenerator


class SensitiveDataGenerator(BaseGenerator):
    """
    Генератор чувствительных данных для режима 'Чувствительные данные'.
    """

    def __init__(self, locale: str = "ru_RU"):
        super().__init__(locale)
        self.fake = Faker(locale)
        self._init_russian_formats()

    def _init_russian_formats(self):
        """Инициализация российских форматов данных"""
        self.passport_series = ['45', '46', '47', '48', '49', '50']
        self.inn_prefixes = ['77', '50', '52', '53']  # Московские регионы

    def generate_credit_card(self) -> Dict[str, Any]:
        """Генерация данных кредитной карты"""
        card_number = self.fake.credit_card_number()
        return {
            "type": "credit_card",
            "card_number": card_number,
            "expiry_date": self.fake.credit_card_expire(),
            "card_holder": self.fake.name().upper(),
            "cvv": self.fake.credit_card_security_code(),
            "provider": self.fake.credit_card_provider(),
            "masked_number": self.mask_credit_card(card_number)
        }

    def generate_passport_data(self) -> Dict[str, Any]:
        """Генерация паспортных данных РФ"""
        series = random.choice(self.passport_series)
        number = self.fake.random_number(digits=6, fix_len=True)
        return {
            "type": "passport",
            "series": series,
            "number": number,
            "full_number": f"{series} {number}",
            "issue_date": self.fake.date_between(start_date='-10y', end_date='-1y').isoformat(),
            "issue_authority": self.fake.random_element(elements=
                ["ОУФМС России по г. Москве", "ГУ МВД России по Московской области", 
                 "ОУФМС России по г. Санкт-Петербургу"]),
            "birth_place": self.fake.city() + " гор.",
            "masked_number": f"{series} ******"
        }

    def generate_inn_snils(self) -> Dict[str, Any]:
        """Генерация ИНН и СНИЛС"""
        inn = self._generate_inn()
        snils = self._generate_snils()
        return {
            "type": "inn_snils",
            "inn": inn,
            "snils": snils,
            "masked_inn": self.mask_string(inn, 4, 4),
            "masked_snils": self.mask_string(snils, 3, 4)
        }

    def generate_medical_data(self) -> Dict[str, Any]:
        """Генерация медицинских данных"""
        blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        return {
            "type": "medical",
            "patient_id": self.fake.uuid4(),
            "blood_type": random.choice(blood_types),
            "allergies": self._generate_allergies(),
            "chronic_diseases": self._generate_chronic_diseases(),
            "last_visit": self.fake.date_between(start_date='-1y', end_date='today').isoformat(),
            "insurance_policy": f"{self.fake.random_number(digits=6, fix_len=True)}",
            "doctor": self.fake.name()
        }

    def _generate_inn(self) -> str:
        """Генерация валидного ИНН"""
        prefix = random.choice(self.inn_prefixes)
        base = f"{prefix}{self.fake.random_number(digits=9, fix_len=True)}"
        # Упрощенная проверка контрольной суммы
        return f"{base}{str(self.fake.random_digit())}"

    def _generate_snils(self) -> str:
        """Генерация СНИЛС"""
        base = str(self.fake.random_number(digits=9, fix_len=True))
        control = str(self.fake.random_number(digits=2, fix_len=True))  # 2 контрольные цифры
        return f"{base[:3]}-{base[3:6]}-{base[6:9]} {base[9:]}"

    def _generate_allergies(self) -> List[str]:
        """Генерация списка аллергий"""
        allergies = ['Пенициллин', 'Аспирин', 'Пыльца', 'Кошка', 'Арахис', 'Молоко', 'Яйца']
        return random.sample(allergies, random.randint(0, 3))

    def _generate_chronic_diseases(self) -> List[str]:
        """Генерация списка хронических заболеваний"""
        diseases = ['Гипертония', 'Диабет 2 типа', 'Астма', 'Артрит', 'Мигрень']
        return random.sample(diseases, random.randint(0, 2))

    def mask_credit_card(self, card_number: str) -> str:
        """Маскировка номера кредитной карты"""
        return card_number[:6] + '*' * (len(card_number) - 10) + card_number[-4:]

    def mask_string(self, text: str, visible_start: int, visible_end: int) -> str:
        """Общая функция маскировки строки"""
        if len(text) <= visible_start + visible_end:
            return text
        return text[:visible_start] + '*' * (len(text) - visible_start - visible_end) + text[-visible_end:]

    def generate_row(self) -> Dict[str, Any]:
        """
        Генерирует чувствительные данные одного типа.
        """
        data_type = random.choice(['credit_card', 'passport', 'inn_snils', 'medical'])
        
        if data_type == 'credit_card':
            return self.generate_credit_card()
        elif data_type == 'passport':
            return self.generate_passport_data()
        elif data_type == 'inn_snils':
            return self.generate_inn_snils()
        else:
            return self.generate_medical_data()

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """
        Проверяет валидность чувствительных данных.
        """
        required_fields = ['type']
        
        # Проверяем наличие обязательных полей
        for field in required_fields:
            if field not in data or not data[field]:
                return False

        # Проверяем корректность типа данных
        if data['type'] not in ['credit_card', 'passport', 'inn_snils', 'medical']:
            return False

        # Дополнительные проверки для каждого типа
        if data['type'] == 'credit_card':
            return len(data.get('card_number', '')) >= 13
        elif data['type'] == 'passport':
            full_number = data.get('full_number', '').replace(' ', '')
            return len(full_number) == 10 and full_number.isdigit()
        elif data['type'] == 'inn_snils':
            return len(data.get('inn', '')) == 12 and len(data.get('snils', '')) >= 11

        return True

    @property
    def generator_type(self) -> str:
        return "sensitive_data"

    def get_supported_fields(self) -> List[str]:
        return [
            "type", "card_number", "expiry_date", "card_holder", "cvv",
            "series", "number", "full_number", "issue_date", "issue_authority",
            "inn", "snils", "patient_id", "blood_type", "allergies", 
            "chronic_diseases", "insurance_policy", "masked_number",
            "masked_inn", "masked_snils"
        ]

    def get_data_types(self) -> List[str]:
        """Возвращает список поддерживаемых типов чувствительных данных"""
        return ['credit_card', 'passport', 'inn_snils', 'medical']