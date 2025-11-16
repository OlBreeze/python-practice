import logging
import os
from datetime import datetime


class ColoredFormatter(logging.Formatter):
    """Кастомний форматер з кольорами для консолі"""

    COLORS = {
        'DEBUG': '\033[36m',  # Cyan
        'INFO': '\033[32m',  # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',  # Red
        'CRITICAL': '\033[35m',  # Magenta
        'RESET': '\033[0m'  # Reset
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        record.levelname = f"{log_color}{record.levelname}{self.COLORS['RESET']}"
        return super().format(record)


class DatabaseLogHandler(logging.Handler):
    """Кастомний хендлер для логування в базу даних"""

    def emit(self, record):
        from .models import LogEntry  # Потрібно створити модель

        try:
            LogEntry.objects.create(
                level=record.levelname,
                message=self.format(record),
                logger_name=record.name,
                module=record.module,
                function=record.funcName,
                line=record.lineno,
            )
        except Exception:
            self.handleError(record)


