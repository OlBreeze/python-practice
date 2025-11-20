from datetime import datetime

from ninja import Schema


class CourseIn(Schema):
    name: str
    description: str
    credits: int


class CourseOut(Schema):
    id: int
    name: str
    description: str
    credits: int


class StudentIn(Schema):
    student_id: str


class StudentOut(Schema):
    id: int
    student_id: str


class GradeIn(Schema):
    enrollment_id: int
    grade: float
    exam_date: datetime


class GradeOut(Schema):
    id: int
    enrollment_id: int
    grade: float
    exam_date: datetime
