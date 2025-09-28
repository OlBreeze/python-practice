#!/usr/bin/env python3
"""
Анализатор лог-файла веб-сервера

Программа анализирует лог-файл веб-сервера в формате Common Log Format (CLF)
или Combined Log Format и выводит статистику по количеству запросов с различных IP-адрес.

Автор: Assistant
Версия: 1.0
"""

import re
from collections import Counter, defaultdict
from typing import Dict, List, Tuple, Optional, NamedTuple
from pathlib import Path


class LogEntry(NamedTuple):
    """
    Структура для представления записи в лог-файле.

    Attributes:
        ip: IP-адрес клиента
        timestamp: Время запроса
        method: HTTP метод (GET, POST, etc.)
        url: Запрашиваемый URL
        status_code: HTTP статус код ответа
        response_size: Размер ответа в байтах
        user_agent: User-Agent клиента (опционально)
    """
    ip: str
    timestamp: str
    method: str
    url: str
    status_code: str
    response_size: str
    user_agent: Optional[str] = None


class LogAnalyzer:
    """
    Класс для анализа лог-файлов веб-сервера.
    """

    def __init__(self, log_file_path: str):
        """
        Инициализация анализатора.

        Args:
            log_file_path: Путь к лог-файлу
        """
        self.log_file_path = Path(log_file_path)
        self.log_entries: List[LogEntry] = []

        # Улучшенное регулярное выражение для Common Log Format (CLF)
        # Формат: host ident authuser [timestamp] "request" status size
        # Пример: 127.0.0.1 - - [25/Dec/2023:10:00:01 +0000] "GET /index.html HTTP/1.1" 200 1234
        self.clf_pattern = re.compile(
            r'^'  # Начало строки
            r'(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|[:\da-fA-F]+)'  # IPv4 или IPv6
            r'\s+'  # Пробелы
            r'(?P<ident>\S+)'  # remote logname (обычно -)
            r'\s+'
            r'(?P<authuser>\S+)'  # remote user (обычно -)
            r'\s+'
            r'\[(?P<timestamp>[^\]]+)\]'  # [timestamp]
            r'\s+'
            r'"(?P<method>[A-Z]+)'  # HTTP метод
            r'\s+'
            r'(?P<url>\S+)'  # URL
            r'\s+'
            r'(?P<protocol>HTTP/[\d\.]+)"'  # HTTP версия
            r'\s+'
            r'(?P<status>\d{3})'  # HTTP статус код
            r'\s+'
            r'(?P<size>\d+|-)'  # Размер ответа в байтах или -
            r'(?:\s+.*)?'  # Возможные дополнительные поля
        )

    def is_valid_ip(self, ip: str) -> bool:
        """
        Проверяет валидность IP адреса.

        Args:
            ip: IP адрес для проверки

        Returns:
            True если IP валидный, False иначе
        """
        # Проверка IPv4
        if self.valid_ipv4_pattern.match(ip):
            return True

        # Простая проверка IPv6 (может быть расширена)
        if ':' in ip and len(ip) > 2:
            return True

        return False

    def parse_log_line(self, line: str) -> Optional[LogEntry]:
        """
        Парсит одну строку лог-файла используя регулярные выражения.

        Args:
            line: Строка из лог-файла

        Returns:
            LogEntry или None, если строка не соответствует формату
        """
        line = line.strip()
        if not line or line.startswith('#'):  # Пропускаем пустые строки и комментарии
            return None

        # Пытаемся сначала Combined Log Format (более полный формат)
        match = self.combined_pattern.match(line)
        if match:
            groups = match.groupdict()
            ip = groups['ip']

            # Проверяем валидность IP адреса
            if not self.is_valid_ip(ip):
                return None

            return LogEntry(
                ip=ip,
                timestamp=groups['timestamp'],
                method=groups['method'],
                url=groups['url'],
                status_code=groups['status'],
                response_size=groups['size'] if groups['size'] != '-' else '0',
                user_agent=groups['user_agent']
            )

        # Если Combined не подошел, пытаемся Common Log Format
        match = self.clf_pattern.match(line)
        if match:
            groups = match.groupdict()
            ip = groups['ip']

            # Проверяем валидность IP адреса
            if not self.is_valid_ip(ip):
                return None

            return LogEntry(
                ip=ip,
                timestamp=groups['timestamp'],
                method=groups['method'],
                url=groups['url'],
                status_code=groups['status'],
                response_size=groups['size'] if groups['size'] != '-' else '0'
            )

        # Если стандартные форматы не подошли, пытаемся извлечь хотя бы IP
        ip_match = self.ip_only_pattern.search(line)
        if ip_match:
            ip = ip_match.group('ip')
            if self.is_valid_ip(ip):
                # Создаем минимальную запись только с IP
                return LogEntry(
                    ip=ip,
                    timestamp='Unknown',
                    method='UNKNOWN',
                    url='/',
                    status_code='000',
                    response_size='0'
                )

        return None

    def load_log_file(self) -> None:
        """
        Загружает и парсит лог-файл.

        Raises:
            FileNotFoundError: Если файл не найден
            PermissionError: Если нет прав на чтение файла
        """
        if not self.log_file_path.exists():
            raise FileNotFoundError(f"Лог-файл не найден: {self.log_file_path}")

        try:
            with open(self.log_file_path, 'r', encoding='utf-8') as file:
                for line_number, line in enumerate(file, 1):
                    try:
                        entry = self.parse_log_line(line)
                        if entry:
                            self.log_entries.append(entry)
                        else:
                            print(f"Предупреждение: не удалось парсить строку {line_number}")
                    except Exception as e:
                        print(f"Ошибка при парсинге строки {line_number}: {e}")

        except PermissionError:
            raise PermissionError(f"Нет прав на чтение файла: {self.log_file_path}")

    def get_ip_statistics(self) -> Counter:
        """
        Вычисляет статистику по IP-адресам.

        Returns:
            Counter с количеством запросов для каждого IP
        """
        return Counter(entry.ip for entry in self.log_entries)

    def get_status_code_statistics(self) -> Counter:
        """
        Вычисляет статистику по HTTP статус-кодам.

        Returns:
            Counter с количеством ответов для каждого статус-кода
        """
        return Counter(entry.status_code for entry in self.log_entries)

    def get_method_statistics(self) -> Counter:
        """
        Вычисляет статистику по HTTP методам.

        Returns:
            Counter с количеством запросов для каждого метода
        """
        return Counter(entry.method for entry in self.log_entries)

    def get_top_urls(self, limit: int = 10) -> List[Tuple[str, int]]:
        """
        Возвращает топ наиболее запрашиваемых URL.

        Args:
            limit: Количество URL для возврата

        Returns:
            Список кортежей (URL, количество_запросов)
        """
        url_counter = Counter(entry.url for entry in self.log_entries)
        return url_counter.most_common(limit)

    def get_hourly_statistics(self) -> Dict[str, int]:
        """
        Вычисляет статистику по часам.

        Returns:
            Словарь с количеством запросов по часам
        """
        hourly_stats = defaultdict(int)

        # Регулярное выражение для извлечения часа из timestamp
        # Поддерживает различные форматы: [25/Dec/2023:10:00:01 +0000] или 2023-12-25 10:00:01
        hour_pattern = re.compile(r'(\d{2}):\d{2}:\d{2}')

        for entry in self.log_entries:
            hour_match = hour_pattern.search(entry.timestamp)
            if hour_match:
                hour = hour_match.group(1)
                hourly_stats[f"{hour}:00"] += 1

        return dict(hourly_stats)

    def analyze_user_agents(self) -> Dict[str, int]:
        """
        Анализирует User-Agent строки и группирует по браузерам.

        Returns:
            Словарь с количеством запросов по браузерам
        """
        browser_stats = defaultdict(int)

        # Регулярные выражения для определения браузеров
        browser_patterns = {
            'Chrome': re.compile(r'Chrome/[\d.]+', re.IGNORECASE),
            'Firefox': re.compile(r'Firefox/[\d.]+', re.IGNORECASE),
            'Safari': re.compile(r'Safari/[\d.]+', re.IGNORECASE),
            'Edge': re.compile(r'Edge/[\d.]+', re.IGNORECASE),
            'Internet Explorer': re.compile(r'MSIE\s[\d.]+', re.IGNORECASE),
            'Opera': re.compile(r'Opera/[\d.]+', re.IGNORECASE),
            'Bot': re.compile(r'bot|crawler|spider|scraper', re.IGNORECASE),
        }

        for entry in self.log_entries:
            if entry.user_agent and entry.user_agent != '-':
                browser_found = False
                for browser_name, pattern in browser_patterns.items():
                    if pattern.search(entry.user_agent):
                        browser_stats[browser_name] += 1
                        browser_found = True
                        break

                if not browser_found:
                    browser_stats['Other'] += 1
            else:
                browser_stats['Unknown'] += 1

        return dict(browser_stats)

    def find_suspicious_ips(self, min_requests: int = 100) -> List[Tuple[str, int, List[str]]]:
        """
        Находит подозрительные IP адреса на основе количества запросов и паттернов.

        Args:
            min_requests: Минимальное количество запросов для подозрительности

        Returns:
            Список кортежей (IP, количество_запросов, список_подозрительных_паттернов)
        """
        ip_stats = self.get_ip_statistics()
        suspicious_ips = []

        # Регулярные выражения для подозрительных паттернов в URL
        suspicious_patterns = {
            'SQL Injection': re.compile(r'(union|select|insert|delete|drop|script)', re.IGNORECASE),
            'XSS Attempt': re.compile(r'(<script|javascript:|onload=|onerror=)', re.IGNORECASE),
            'Directory Traversal': re.compile(r'(\.\./|\.\.\\|/etc/passwd|/windows/system32)', re.IGNORECASE),
            'Admin Panel Access': re.compile(r'(admin|wp-admin|administrator|dashboard)', re.IGNORECASE),
            'Config Files': re.compile(r'(\.env|config\.php|wp-config|database)', re.IGNORECASE),
        }

        for ip, count in ip_stats.items():
            if count >= min_requests:
                # Анализируем запросы от этого IP
                ip_requests = [entry for entry in self.log_entries if entry.ip == ip]
                found_patterns = []

                for entry in ip_requests:
                    for pattern_name, pattern in suspicious_patterns.items():
                        if pattern.search(entry.url) and pattern_name not in found_patterns:
                            found_patterns.append(pattern_name)

                if found_patterns or count > 1000:  # Много запросов тоже подозрительно
                    if count > 1000:
                        found_patterns.append('High Request Volume')
                    suspicious_ips.append((ip, count, found_patterns))

        return sorted(suspicious_ips, key=lambda x: x[1], reverse=True)  # Конец строки

        # Улучшенное регулярное выражение для Combined Log Format
        # Формат: CLF + "referer" "user-agent"
        self.combined_pattern = re.compile(
        r'^'  # Начало строки
        r'(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|[:\da-fA-F]+)'  # IPv4 или IPv6
        r'\s+'
        r'(?P<ident>\S+)'  # remote logname
        r'\s+'
        r'(?P<authuser>\S+)'  # remote user
        r'\s+'
        r'\[(?P<timestamp>[^\]]+)\]'  # timestamp
        r'\s+'
        r'"(?P<method>[A-Z]+)'  # HTTP метод
        r'\s+'
        r'(?P<url>\S+)'  # URL
        r'\s+'
        r'(?P<protocol>HTTP/[\d\.]+)"'  # HTTP версия
        r'\s+'
        r'(?P<status>\d{3})'  # HTTP статус код
        r'\s+'
        r'(?P<size>\d+|-)'  # Размер ответа
        r'\s+'
        r'"(?P<referer>[^"]*)"'  # Referer
        r'\s+'
        r'"(?P<user_agent>[^"]*)"'  # User-Agent
        r'(?:\s+.*)?'  # Дополнительные поля
        )


def parse_log_line(self, line: str) -> Optional[LogEntry]:
    """
    Парсит одну строку лог-файла.

    Args:
        line: Строка из лог-файла

    Returns:
        LogEntry или None, если строка не соответствует формату
    """
    line = line.strip()
    if not line:
        return None

    # Пытаемся сначала Combined Log Format
    match = self.combined_pattern.match(line)
    if match:
        ip, timestamp, method, url, status_code, response_size, user_agent = match.groups()
        return LogEntry(ip, timestamp, method, url, status_code, response_size, user_agent)

    # Если не подходит, пытаемся Common Log Format
    match = self.clf_pattern.match(line)
    if match:
        ip, timestamp, method, url, status_code, response_size = match.groups()
        return LogEntry(ip, timestamp, method, url, status_code, response_size)

    return None


def load_log_file(self) -> None:
    """
    Загружает и парсит лог-файл.

    Raises:
        FileNotFoundError: Если файл не найден
        PermissionError: Если нет прав на чтение файла
    """
    if not self.log_file_path.exists():
        raise FileNotFoundError(f"Лог-файл не найден: {self.log_file_path}")

    try:
        with open(self.log_file_path, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, 1):
                try:
                    entry = self.parse_log_line(line)
                    if entry:
                        self.log_entries.append(entry)
                    else:
                        print(f"Предупреждение: не удалось парсить строку {line_number}")
                except Exception as e:
                    print(f"Ошибка при парсинге строки {line_number}: {e}")

    except PermissionError:
        raise PermissionError(f"Нет прав на чтение файла: {self.log_file_path}")


def get_ip_statistics(self) -> Counter:
    """
    Вычисляет статистику по IP-адресам.

    Returns:
        Counter с количеством запросов для каждого IP
    """
    return Counter(entry.ip for entry in self.log_entries)


def get_status_code_statistics(self) -> Counter:
    """
    Вычисляет статистику по HTTP статус-кодам.

    Returns:
        Counter с количеством ответов для каждого статус-кода
    """
    return Counter(entry.status_code for entry in self.log_entries)


def get_method_statistics(self) -> Counter:
    """
    Вычисляет статистику по HTTP методам.

    Returns:
        Counter с количеством запросов для каждого метода
    """
    return Counter(entry.method for entry in self.log_entries)


def get_top_urls(self, limit: int = 10) -> List[Tuple[str, int]]:
    """
    Возвращает топ наиболее запрашиваемых URL.

    Args:
        limit: Количество URL для возврата

    Returns:
        Список кортежей (URL, количество_запросов)
    """
    url_counter = Counter(entry.url for entry in self.log_entries)
    return url_counter.most_common(limit)


def get_hourly_statistics(self) -> Dict[str, int]:
    """
    Вычисляет статистику по часам.

    Returns:
        Словарь с количеством запросов по часам
    """
    hourly_stats = defaultdict(int)

    # for entry in self.log_  # Конец строки
    #     )

        # Простое регулярное выражение для извлечения только IP адресов
        # Полезно для нестандартных форматов логов
        # self.ip_only_pattern = re.compile(r'(?P<ip>\b(?:\d{1,3}\.){3}\d{1,3}\b|(?:[a-fA-F0-9]*:+)+[a-fA-F0-9]+)')

# Регулярное выражение для проверки валидности IP адресов
# self.valid_ipv4_pattern = re.compile(
# r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}'
# r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)


def parse_log_line(self, line: str) -> Optional[LogEntry]:
    """
    Парсит одну строку лог-файла.

    Args:
        line: Строка из лог-файла

    Returns:
        LogEntry или None, если строка не соответствует формату
    """
    line = line.strip()
    if not line:
        return None

    # Пытаемся сначала Combined Log Format
    match = self.combined_pattern.match(line)
    if match:
        ip, timestamp, method, url, status_code, response_size, user_agent = match.groups()
        return LogEntry(ip, timestamp, method, url, status_code, response_size, user_agent)

    # Если не подходит, пытаемся Common Log Format
    match = self.clf_pattern.match(line)
    if match:
        ip, timestamp, method, url, status_code, response_size = match.groups()
        return LogEntry(ip, timestamp, method, url, status_code, response_size)

    return None


def load_log_file(self) -> None:
    """
    Загружает и парсит лог-файл.

    Raises:
        FileNotFoundError: Если файл не найден
        PermissionError: Если нет прав на чтение файла
    """
    if not self.log_file_path.exists():
        raise FileNotFoundError(f"Лог-файл не найден: {self.log_file_path}")

    try:
        with open(self.log_file_path, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, 1):
                try:
                    entry = self.parse_log_line(line)
                    if entry:
                        self.log_entries.append(entry)
                    else:
                        print(f"Предупреждение: не удалось парсить строку {line_number}")
                except Exception as e:
                    print(f"Ошибка при парсинге строки {line_number}: {e}")

    except PermissionError:
        raise PermissionError(f"Нет прав на чтение файла: {self.log_file_path}")


def get_ip_statistics(self) -> Counter:
    """
    Вычисляет статистику по IP-адресам.

    Returns:
        Counter с количеством запросов для каждого IP
    """
    return Counter(entry.ip for entry in self.log_entries)


def get_status_code_statistics(self) -> Counter:
    """
    Вычисляет статистику по HTTP статус-кодам.

    Returns:
        Counter с количеством ответов для каждого статус-кода
    """
    return Counter(entry.status_code for entry in self.log_entries)


def get_method_statistics(self) -> Counter:
    """
    Вычисляет статистику по HTTP методам.

    Returns:
        Counter с количеством запросов для каждого метода
    """
    return Counter(entry.method for entry in self.log_entries)


def get_top_urls(self, limit: int = 10) -> List[Tuple[str, int]]:
    """
    Возвращает топ наиболее запрашиваемых URL.

    Args:
        limit: Количество URL для возврата

    Returns:
        Список кортежей (URL, количество_запросов)
    """
    url_counter = Counter(entry.url for entry in self.log_entries)
    return url_counter.most_common(limit)
