import sys
import os

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from generators import factory


def test_user_generator():
    print("🧪 Тестируем генератор пользователей...")

    generator = factory.create_generator("user")
    assert generator is not None, "Генератор не создан"

    # Тестируем одну строку
    row = generator.generate_row()
    print("✅ Одна строка сгенерирована:")
    for key, value in row.items():
        print(f"   {key}: {value}")

    # Тестируем валидацию
    is_valid = generator.validate_data(row)
    print(f"✅ Валидация данных: {is_valid}")

    # Тестируем пакетную генерацию
    batch = generator.generate_batch(2)
    print(f"✅ Пакетная генерация: {len(batch)} строк")

    print("🎉 Все тесты пройдены!")


def test_vulnerability_generator():
    print("\n🧪 Тестируем генератор уязвимостей...")

    generator = factory.create_generator("vulnerability")
    assert generator is not None, "Генератор уязвимостей не создан"

    # Тестируем общую генерацию
    row = generator.generate_row()
    print("✅ Общая генерация уязвимости:")
    for key, value in row.items():
        print(f"   {key}: {value}")

    # Тестируем валидацию
    is_valid = generator.validate_data(row)
    print(f"✅ Валидация данных: {is_valid}")

    # Тестируем специфические генераторы
    sql_data = generator.generate_sql_injection()
    print(f"✅ SQL-инъекция: {sql_data['payload']}")

    xss_data = generator.generate_xss_payload()
    print(f"✅ XSS payload: {xss_data['payload']}")

    path_data = generator.generate_path_traversal()
    print(f"✅ Path Traversal: {path_data['payload']}")

    # Тестируем пакетную генерацию
    batch = generator.generate_batch(3)
    print(f"✅ Пакетная генерация: {len(batch)} строк уязвимостей")

    # Проверяем поддерживаемые типы уязвимостей
    vuln_types = generator.get_vulnerability_types()
    print(f"✅ Поддерживаемые типы уязвимостей: {vuln_types}")

    # Проверяем поддерживаемые поля
    supported_fields = generator.get_supported_fields()
    print(f"✅ Поддерживаемые поля: {supported_fields}")

    print("🎉 Все тесты генератора уязвимостей пройдены!")


if __name__ == "__main__":
    test_user_generator()
    test_vulnerability_generator()