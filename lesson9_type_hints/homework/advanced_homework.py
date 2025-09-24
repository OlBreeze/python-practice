# ПРОВЕРКА КОДА!!!
# 📋 Пошагова інструкція
# Крок 1: Встановлення інструментів
# pip install mypy
# pip install pyright

# Крок 2: Перевірка через mypy
# # Перевірка конкретного файлу
# mypy advanced_homework.py
#
# # Перевірка всіх Python файлів у директорії
# mypy .
#
# # Детальна перевірка з додатковими опціями
# mypy --strict advanced_homework.py
#
# # Перевірка з генерацією звіту
# mypy --html-report mypy_report advanced_homework.py


# Крок 3: Перевірка через pyright
# # Перевірка конкретного файлу
# pyright advanced_homework.py
#
# # Перевірка всіх файлів
# pyright
#
# # Детальна перевірка
# pyright --verbose advanced_homework.py
#
# # Перевірка з конфігурацією
# pyright --project .
# ⚙️ Конфігурація інструментів
# mypy.ini (конфігурація mypy):
# [mypy]
# python_version = 3.9
# warn_return_any = True
# warn_unused_configs = True
# disallow_untyped_defs = True
# disallow_incomplete_defs = True
# check_untyped_defs = True
# disallow_untyped_decorators = True
# no_implicit_optional = True
# warn_redundant_casts = True
# warn_unused_ignores = True
# warn_no_return = True
# warn_unreachable = True
# strict_equality = True
# pyrightconfig.json (конфігурація pyright):
# {
#   "include": [
#     "."
#   ],
#   "exclude": [
#     "**/node_modules",
#     "**/__pycache__"
#   ],
#   "typeCheckingMode": "strict",
#   "pythonVersion": "3.9",
#   "reportMissingTypeStubs": false,
#   "reportImportCycles": true,
#   "reportUnusedImport": true,
#   "reportUnusedVariable": true
# }

# # Строга перевірка mypy
# mypy --strict advanced_homework.py
#
# # Перевірка pyright
# pyright advanced_homework.py
#
# # Детальна перевірка pyright
# pyright --verbose advanced_homework.py

