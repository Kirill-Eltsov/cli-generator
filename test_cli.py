#!/usr/bin/env python3
"""
Тестирование CLI интерфейса
"""

import sys
import os

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cli.commands import cli


def test_commands():
    """Тестируем основные команды"""
    print("🧪 Тестирование CLI команд...")

    # Тестируем список генераторов
    print("\n1. Тестируем list-generators:")
    try:
        cli(['list-generators'])
    except SystemExit:
        pass

    # Тестируем генерацию данных
    print("\n2. Тестируем generate команду:")
    try:
        cli(['generate', '--type', 'user', '--rows', '2', '--format', 'json'])
    except SystemExit:
        pass

    print("\n🎉 Тестирование завершено!")


if __name__ == '__main__':
    test_commands()