from ninja import Schema
from datetime import datetime


class TaskIn(Schema):
    title: str
    description: str
    status: str
    due_date: datetime


class TaskOut(Schema):
    id: int
    title: str
    description: str
    status: str
    created_at: datetime
    due_date: datetime