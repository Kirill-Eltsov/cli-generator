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


if __name__ == "__main__":
    test_user_generator()