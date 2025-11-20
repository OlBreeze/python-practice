from datetime import datetime
from ninja import Schema


class PostIn(Schema):
    title: str
    content: str


class PostOut(Schema):
    id: int
    title: str
    content: str
    created_at: datetime


class TagIn(Schema):
    name: str


class TagOut(Schema):
    id: int
    name: str


class CommentIn(Schema):
    text: str


class CommentOut(Schema):
    id: int
    post_id: int
    text: str
    created_at: datetime
