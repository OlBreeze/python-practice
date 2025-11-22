from datetime import datetime

from ninja import Schema


class ServerIn(Schema):
    name: str
    ip_address: str
    status: str


class ServerOut(Schema):
    id: int
    name: str
    ip_address: str
    status: str


class MetricIn(Schema):
    cpu_usage: float
    memory_usage: float
    disk_usage: float


class MetricOut(Schema):
    id: int
    server_id: int
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    timestamp: datetime
