# cli-generator

Генератор тестовых данных для cybersecurity-тестирования.

CLI-инструмент для генерации различных типов тестовых данных, используемых в тестировании безопасности приложений. Поддерживает генерацию пользовательских данных, уязвимостей, чувствительных данных и данных для penetration testing с встроенными payload-ами инъекций.

## Возможности

- **Множество типов генераторов**: user, vulnerability, sensitive_data, penetration
- **Поддержка шаблонов**: генерация только выбранных полей
- **Различные форматы вывода**: JSON, CSV, SQL
- **Маскировка данных**: для защиты чувствительной информации
- **Многоязычная поддержка**: локали Faker
- **Инъекции уязвимостей**: встроенные SQL, XSS, Path Traversal payload-ы
- **Валидация данных**: проверка корректности сгенерированных данных

## Использование

### Основное использование

```bash
# Генерация 10 строк пользовательских данных в JSON формате
datagen generate --type user --rows 10

# Сохранение в файл
datagen generate --type user --rows 100 --output users.json

# Генерация в CSV формате
datagen generate --type penetration --format csv --rows 50 --output penetration_data.csv
```

### Доступные команды

#### generate

Генерирует тестовые данные указанного типа.

Опции:
- `--type, -t`: тип данных (user, vulnerability, sensitive_data, penetration) [default: user]
- `--format, -f`: формат вывода (json, csv, sql) [default: json]
- `--rows, -r`: количество строк [default: 10]
- `--output, -o`: имя выходного файла
- `--mode`: режим работы (standard, vulnerability, penetration) [default: standard]
- `--locale`: локаль для генерации [default: ru_RU]
- `--mask`: маскировать чувствительные данные
- `--template, -T`: путь к JSON-файлу с шаблоном полей

#### list-generators

Показывает список доступных генераторов и количество поддерживаемых полей.

```bash
datagen list-generators
```

#### test

Тестирует указанный генератор, выводя сгенерированные данные на экран.

```bash
datagen test --type penetration --rows 3
```

## Примеры

### Генерация пользовательских данных

```bash
# Простая генерация
datagen generate --type user --rows 5

# С сохранением в SQL файл
datagen generate --type user --rows 100 --format sql --output users.sql

# С маскировкой
datagen generate --type user --rows 50 --mask --output masked_users.json
```

### Penetration Testing данные

```bash
# Генерация данных с инъекциями
datagen generate --type penetration --rows 20 --output pentest_data.json

# В CSV формате
datagen generate --type penetration --format csv --rows 100 --output injections.csv
```

### Использование шаблонов

Шаблоны позволяют генерировать только выбранные поля.

#### Формат шаблона

Шаблон - это JSON-файл со следующей структурой:

```json
{
  "name": "custom_user",
  "description": "Шаблон для генерации пользовательских данных",
  "fields": ["id", "username", "email", "phone"]
}
```

- `name`: Имя шаблона (строка)
- `description`: Описание шаблона (опционально, строка)
- `fields`: Список имен полей для генерации (массив строк)

#### Пример использования

1. Используйте пример шаблона `templates/example_template.json` или создайте свой `template.json`:

```json
{
  "name": "basic_user",
  "fields": ["id", "username", "email", "phone"]
}
```

2. Запустите генерацию с шаблоном:

```bash
datagen generate --type user --rows 10 --template templates/example_template.json --output custom_users.json
```

Это сгенерирует только поля `id`, `username`, `email` и `phone` из генератора user.

### Тестирование генераторов

```bash
# Просмотр доступных генераторов
datagen list-generators

# Тестирование генератора user
datagen test --type user --rows 2

# Тестирование penetration генератора
datagen test --type penetration --rows 3
```

## Генераторы данных

### User Generator

Генерирует стандартные пользовательские данные:
- `id`, `username`, `first_name`, `last_name`
- `email`, `phone`, `address`
- `birth_date`, `company`, `job`
- `credit_card` (number, expiry, provider)

### Penetration Generator

Генерирует данные для тестирования уязвимостей с встроенными payload-ами:
- **SQL Injection**: `' OR '1'='1`, `' UNION SELECT username, password FROM users--`, etc.
- **XSS**: `<script>alert('XSS')</script>`, `<img src=x onerror=alert('XSS')>`, etc.
- **Path Traversal**: `../../../etc/passwd`, `..\\..\\..\\windows\\system32\\drivers\\etc\\hosts`, etc.

Включает метаданные: `injected_fields`, `total_injections`, `injection_types`.

### Доступные поля

Список доступных полей зависит от типа генератора. Используйте команду `list-generators` для просмотра:

```bash
datagen list-generators
```

### Другие генераторы

- **Vulnerability Generator**: данные о уязвимостях
- **Sensitive Data Generator**: чувствительные данные

## Конфигурация

### Локали

Поддерживаемые локали через Faker:
- `ru_RU` (по умолчанию)
- `en_US`, `de_DE`, `fr_FR`, etc.

```bash
datagen generate --type user --locale en_US --rows 10
```

## Лицензия

MIT License
