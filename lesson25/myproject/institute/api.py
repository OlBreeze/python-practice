from ninja import Router
from django.shortcuts import get_object_or_404
from typing import List
from .models import *
from .schemas import *

router = Router()

@router.get("/courses", response=List[CourseOut])
def list_courses(request):
    return Course.objects.all()


@router.post("/courses", response=CourseOut)
def create_course(request, payload: CourseIn):
    course = Course.objects.create(**payload.dict())
    return course


@router.get("/courses/{course_id}", response=CourseOut)
def get_course(request, course_id: int):
    return get_object_or_404(Course, id=course_id)


@router.put("/courses/{course_id}", response=CourseOut)
def update_course(request, course_id: int, payload: CourseIn):
    course = get_object_or_404(Course, id=course_id)
    for attr, value in payload.dict().items():
        setattr(course, attr, value)
    course.save()
    return course


@router.delete("/courses/{course_id}")
def delete_course(request, course_id: int):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    return {"success": True}


@router.get("/students", response=List[StudentOut])
def list_students(request):
    return Student.objects.all()


@router.post("/students", response=StudentOut)
def create_student(request, payload: StudentIn):
    student = Student.objects.create(user=request.user, **payload.dict())
    return student


@router.post("/enrollments")
def enroll_student(request, student_id: int, course_id: int):
    student = get_object_or_404(Student, id=student_id)
    course = get_object_or_404(Course, id=course_id)
    enrollment = Enrollment.objects.create(student=student, course=course)
    return {"success": True, "enrollment_id": enrollment.id}


@router.post("/grades", response=GradeOut)
def add_grade(request, payload: GradeIn):
    grade = Grade.objects.create(**payload.dict())
    return grade


@router.get("/courses/{course_id}/average")
def get_course_average(request, course_id: int):
    enrollments = Enrollment.objects.filter(course_id=course_id)
    grades = Grade.objects.filter(enrollment__in=enrollments)
    if grades.exists():
        avg = sum(g.grade for g in grades) / len(grades)
        return {"course_id": course_id, "average_grade": avg}
    return {"course_id": course_id, "average_grade": 0}