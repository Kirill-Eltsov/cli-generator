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


def test_sensitive_data_generator():
    print("\n🧪 Тестируем генератор чувствительных данных...")

    generator = factory.create_generator("sensitive_data")
    assert generator is not None, "Генератор чувствительных данных не создан"

    # Тестируем общую генерацию
    row = generator.generate_row()
    print(f"✅ Общая генерация ({row['type']}):")
    for key, value in row.items():
        print(f"   {key}: {value}")

    # Тестируем валидацию
    is_valid = generator.validate_data(row)
    print(f"✅ Валидация данных: {is_valid}")

    # Тестируем специфические генераторы
    credit_card_data = generator.generate_credit_card()
    print(f"✅ Кредитная карта: {credit_card_data['masked_number']}")

    passport_data = generator.generate_passport_data()
    print(f"✅ Паспорт: {passport_data['masked_number']}")

    inn_snils_data = generator.generate_inn_snils()
    print(f"✅ ИНН/СНИЛС: {inn_snils_data['masked_inn']} / {inn_snils_data['masked_snils']}")

    medical_data = generator.generate_medical_data()
    print(f"✅ Мед. данные: {medical_data['blood_type']}, аллергии: {len(medical_data['allergies'])}")

    # Тестируем пакетную генерацию
    batch = generator.generate_batch(4)
    print(f"✅ Пакетная генерация: {len(batch)} строк чувствительных данных")

    # Тестируем функцию маскировки
    test_card = "1234567890123456"
    masked_card = generator.mask_credit_card(test_card)
    print(f"✅ Маскировка карты: {test_card} -> {masked_card}")

    test_string = "1234567890"
    masked_string = generator.mask_string(test_string, 2, 3)
    print(f"✅ Маскировка строки: {test_string} -> {masked_string}")

    # Проверяем поддерживаемые типы данных
    data_types = generator.get_data_types()
    print(f"✅ Поддерживаемые типы данных: {data_types}")

    # Проверяем поддерживаемые поля
    supported_fields = generator.get_supported_fields()
    print(f"✅ Поддерживаемые поля: {len(supported_fields)}")

    print("🎉 Все тесты генератора чувствительных данных пройдены!")


def test_penetration_generator():
    print("\n🧪 Тестируем генератор penetration testing...")

    generator = factory.create_generator("penetration")
    assert generator is not None, "Генератор penetration не создан"

    # Тестируем генерацию строки
    row = generator.generate_row()
    print("✅ Строка сгенерирована:")
    for key in sorted(row.keys()):
        print(f"   {key}: {row[key]}")

    # Тестируем валидацию
    is_valid = generator.validate_data(row)
    print(f"✅ Валидация данных: {is_valid}")

    # Проверяем обязательные поля
    required_fields = ['id', 'timestamp', 'source_ip']
    for field in required_fields:
        assert field in row, f"Обязательное поле {field} отсутствует"
        assert row[field], f"Обязательное поле {field} пустое"

    # Проверяем инъекции
    injected_fields = row.get('injected_fields', [])
    total_injections = row.get('total_injections', 0)
    injection_types = row.get('injection_types', [])

    print(f"✅ Инъекции: {total_injections} в полях {injected_fields}")
    print(f"✅ Типы инъекций: {injection_types}")

    # Проверяем, что injected_fields соответствуют данным
    for field in injected_fields:
        vuln_type = row.get(f'{field}_vulnerability_type')
        assert vuln_type in generator.payloads, f"Неверный тип уязвимости {vuln_type}"
        assert row[field] in generator.payloads[vuln_type], f"Payload не соответствует типу {vuln_type}"

    # Тестируем пакетную генерацию
    batch = generator.generate_batch(2)
    print(f"✅ Пакетная генерация: {len(batch)} строк")

    for item in batch:
        assert generator.validate_data(item), "Невалидные данные в пакете"

    # Проверяем поддерживаемые поля
    supported_fields = generator.get_supported_fields()
    print(f"✅ Поддерживаемые поля: {len(supported_fields)}")

    # Проверяем, что все поля в поддерживаемых
    for key in row.keys():
        assert key in supported_fields, f"Поле {key} не в поддерживаемых"

    print("🎉 Все тесты генератора penetration пройдены!")


if __name__ == "__main__":
    test_user_generator()
    test_vulnerability_generator()
    test_sensitive_data_generator()
    test_penetration_generator()