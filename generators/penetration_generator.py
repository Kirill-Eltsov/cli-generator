from faker import Faker
from typing import Dict, Any, List
import random
from .base_generator import BaseGenerator


class PenetrationGenerator(BaseGenerator):
    """
    Генератор данных для режима penetration testing.
    Создает комбинированные наборы данных со случайными payload-ами в случайных полях.
    """

    def __init__(self, locale: str = "ru_RU", injection_probability: float = 0.4):
        super().__init__(locale)
        self.fake = Faker(locale)
        self.injection_probability = injection_probability  # Вероятность инъекции payload в поле

        # Инициализация payload-ов из разных типов уязвимостей
        self.payloads = {
            'sql': self._init_sql_payloads(),
            'xss': self._init_xss_payloads(),
            'path_traversal': self._init_path_traversal_payloads()
        }

        # Поля, которые могут содержать инъекции
        self.injectable_fields = [
            'username', 'password', 'email', 'first_name', 'last_name',
            'comment', 'message', 'search_query', 'file_path', 'url',
            'phone', 'address', 'city', 'country', 'description'
        ]

    def _init_sql_payloads(self) -> List[str]:
        """Инициализация SQL-инъекций"""
        return [
            "' OR '1'='1",
            "' UNION SELECT username, password FROM users--",
            "'; DROP TABLE users--",
            "' OR 1=1--",
            "admin'--",
            "' AND 1=CAST((SELECT version()) AS int)--",
            "' WAITFOR DELAY '00:00:10'--",
            "' OR EXISTS(SELECT * FROM information_schema.tables)--"
        ]

    def _init_xss_payloads(self) -> List[str]:
        """Инициализация XSS payload-ов"""
        return [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('XSS')>",
            "javascript:alert('XSS')",
            "<body onload=alert('XSS')>",
            "<iframe src=javascript:alert('XSS')>",
            "<a href=javascript:alert('XSS')>click</a>"
        ]

    def _init_path_traversal_payloads(self) -> List[str]:
        """Инициализация Path Traversal payload-ов"""
        return [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
            "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
            "....//....//....//etc/passwd",
            "../../../etc/shadow",
            "../../../../windows/win.ini"
        ]

    def _get_random_payload(self, payload_type: str) -> str:
        """Получить случайный payload указанного типа"""
        return random.choice(self.payloads[payload_type])

    def _generate_normal_data(self, field: str) -> str:
        """Генерировать нормальные данные для поля"""
        generators = {
            'username': lambda: self.fake.user_name(),
            'password': lambda: self.fake.password(),
            'email': lambda: self.fake.email(),
            'first_name': lambda: self.fake.first_name(),
            'last_name': lambda: self.fake.last_name(),
            'comment': lambda: self.fake.sentence(),
            'message': lambda: self.fake.text(max_nb_chars=100),
            'search_query': lambda: self.fake.word(),
            'file_path': lambda: self.fake.file_path(),
            'url': lambda: self.fake.url(),
            'phone': lambda: self.fake.phone_number(),
            'address': lambda: self.fake.address(),
            'city': lambda: self.fake.city(),
            'country': lambda: self.fake.country(),
            'description': lambda: self.fake.text(max_nb_chars=200)
        }
        return generators.get(field, lambda: self.fake.word())()

    def generate_row(self) -> Dict[str, Any]:
        """
        Генерирует комплексную строку данных с возможными инъекциями в случайных полях.
        """
        row = {
            'id': self.fake.uuid4(),
            'timestamp': self.fake.iso8601(),
            'source_ip': self.fake.ipv4(),
            'user_agent': self.fake.user_agent(),
            'session_id': self.fake.uuid4()
        }

        injected_fields = []

        # Генерируем данные для каждого поля
        for field in self.injectable_fields:
            if random.random() < self.injection_probability:
                # Внедряем payload
                payload_type = random.choice(list(self.payloads.keys()))
                payload = self._get_random_payload(payload_type)
                row[field] = payload
                row[f'{field}_vulnerability_type'] = payload_type
                injected_fields.append(field)
            else:
                # Нормальные данные
                row[field] = self._generate_normal_data(field)

        # Метаданные о инъекциях
        row['injected_fields'] = injected_fields
        row['total_injections'] = len(injected_fields)
        row['injection_types'] = list(set(row.get(f'{field}_vulnerability_type', '') for field in injected_fields))

        return row

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """
        Валидирует сгенерированные данные.
        """
        required_fields = ['id', 'timestamp', 'source_ip']

        # Проверяем наличие обязательных полей
        for field in required_fields:
            if field not in data or not data[field]:
                return False

        # Проверяем корректность инъекций
        injected_fields = data.get('injected_fields', [])
        for field in injected_fields:
            vuln_type = data.get(f'{field}_vulnerability_type')
            if not vuln_type or vuln_type not in self.payloads:
                return False
            if field not in data or data[field] not in self.payloads[vuln_type]:
                return False

        return True

    @property
    def generator_type(self) -> str:
        return "penetration"

    def get_supported_fields(self) -> List[str]:
        fields = [
            "id", "timestamp", "source_ip", "user_agent", "session_id",
            "injected_fields", "total_injections", "injection_types"
        ]
        fields.extend(self.injectable_fields)
        fields.extend([f"{field}_vulnerability_type" for field in self.injectable_fields])
        return fields