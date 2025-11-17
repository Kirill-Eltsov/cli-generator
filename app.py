#!/usr/bin/env python3
"""
Главный модуль для запуска генератора тестовых данных.
"""

import sys
import os

# Добавляем текущую директорию в путь для импорта
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cli.commands import cli

if __name__ == '__main__':
    cli()