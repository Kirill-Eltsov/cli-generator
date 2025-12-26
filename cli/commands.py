import click
import logging
import sys
import os
import json
from typing import Optional

# Добавляем путь для импорта модулей
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    from generators import factory
    from exporters import export_data
    from schemas import validate_user_template, filter_output_by_template
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    print("Убедитесь, что все модули созданы правильно")
    sys.exit(1)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@click.group()
def cli():
    """Генератор тестовых данных для cybersecurity-тестирования"""
    pass


@cli.command()
@click.option('--type', '-t',
              type=click.Choice(['user', 'vulnerability', 'sensitive_data', 'penetration'], case_sensitive=False),
              default='user',
              help='Тип генерируемых данных')
@click.option('--format', '-f',
              type=click.Choice(['csv', 'json', 'sql'], case_sensitive=False),
              default='json',
              help='Формат вывода данных')
@click.option('--rows', '-r',
              default=10,
              help='Количество строк для генерации')
@click.option('--output', '-o',
              help='Имя выходного файла')
@click.option('--mode',
              type=click.Choice(['standard', 'vulnerability', 'penetration'], case_sensitive=False),
              default='standard',
              help='Режим работы генератора')
@click.option('--locale',
              default='ru_RU',
              help='Локаль для генерации данных')
@click.option('--mask', is_flag=True,
              help='Маскировать чувствительные данные')
@click.option('--template', '-T',
              help='Путь к JSON-файлу с шаблоном полей для генерации')
def generate(type: str, format: str, rows: int, output: Optional[str],
             mode: str, locale: str, mask: bool, template: Optional[str]):
    """
    Генерирует тестовые данные в указанном формате.
    """
    try:
        logger.info(f"Запуск генерации: type={type}, format={format}, rows={rows}, mode={mode}, template={template}")

        # Загружаем шаблон если указан
        user_template = None
        if template:
            try:
                with open(template, 'r', encoding='utf-8') as f:
                    template_data = json.load(f)
                user_template = validate_user_template(template_data)
                click.echo(f"📋 Используется шаблон: {user_template.name}")
            except Exception as e:
                click.echo(f"❌ Ошибка загрузки шаблона: {e}")
                return

        # Создаем генератор
        generator = factory.create_generator(type, locale=locale)
        if not generator:
            click.echo(f"❌ Ошибка: Генератор типа '{type}' не найден")
            return

        # Генерируем данные
        click.echo(f"🔄 Генерация {rows} строк данных типа '{type}'...")
        data = generator.generate_batch(rows)

        if not data:
            click.echo("❌ Не удалось сгенерировать данные")
            return

        # Фильтруем данные по шаблону если указан
        if user_template:
            click.echo(f"🔍 Фильтрация данных по полям шаблона: {user_template.fields}")
            data = [filter_output_by_template(row, user_template) for row in data]

        # Экспортируем данные
        click.echo(f"💾 Экспорт данных в формате {format}...")
        result = export_data(data, format, output, mask_data=mask)

        if result:
            click.echo(f"✅ Данные успешно сгенерированы и экспортированы!")
            if output:
                click.echo(f"📁 Файл: {output}")
        else:
            click.echo("❌ Ошибка при экспорте данных")

    except Exception as e:
        logger.error(f"Ошибка при выполнении команды: {e}")
        click.echo(f"❌ Произошла ошибка: {e}")


@cli.command()
def list_generators():
    """Показывает список доступных генераторов"""
    generators = factory.get_available_generators()
    click.echo("📊 Доступные генераторы данных:")
    for gen_type in generators:
        generator = factory.create_generator(gen_type)
        if generator:
            fields = generator.get_supported_fields()
            click.echo(f"  • {gen_type}: {len(fields)} полей")


@cli.command()
@click.option('--type', '-t', required=True,
              help='Тип генератора для тестирования')
@click.option('--rows', '-r', default=3,
              help='Количество тестовых строк')
def test(type: str, rows: int):
    """Тестирует указанный генератор"""
    try:
        generator = factory.create_generator(type)
        if not generator:
            click.echo(f"❌ Генератор '{type}' не найден")
            return

        click.echo(f"🧪 Тестирование генератора '{type}':")
        data = generator.generate_batch(rows)

        for i, row in enumerate(data, 1):
            click.echo(f"\n📝 Строка {i}:")
            for key, value in row.items():
                click.echo(f"   {key}: {value}")

        click.echo(f"\n✅ Успешно сгенерировано {len(data)} строк")

    except Exception as e:
        click.echo(f"❌ Ошибка при тестировании: {e}")

# Убираем блок if __name__ == '__main__' чтобы избежать проблем с импортом