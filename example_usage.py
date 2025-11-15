from generators.generator_factory import factory


def demonstrate_generators():
    # Создаем генератор пользователей
    user_generator = factory.create_generator("user", locale="ru_RU")

    if user_generator:
        print(f"Тип генератора: {user_generator.generator_type}")

        # Генерируем одну строку
        single_row = user_generator.generate_row()
        print("Одна строка данных:")
        print(single_row)

        # Генерируем несколько строк
        batch = user_generator.generate_batch(3)
        print("\nНесколько строк данных:")
        for i, row in enumerate(batch, 1):
            print(f"Строка {i}: {row}")

    # Показываем доступные генераторы
    print(f"\nДоступные генераторы: {factory.get_available_generators()}")


if __name__ == "__main__":
    demonstrate_generators()