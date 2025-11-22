from ninja import Router
from django.shortcuts import get_object_or_404
from typing import List
from .models import *
from .schemas import *

router = Router()

# ============= 1. TASK MANAGER API =============
@router.get("/tasks", response=List[TaskOut])
def list_tasks(request):
    tasks = Task.objects.filter(user=request.user)
    return tasks


@router.post("/tasks", response=TaskOut)
def create_task(request, payload: TaskIn):
    task = Task.objects.create(user=request.user, **payload.dict())
    return task


@router.get("/tasks/{task_id}", response=TaskOut)
def get_task(request, task_id: int):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    return task


@router.put("/tasks/{task_id}", response=TaskOut)
def update_task(request, task_id: int, payload: TaskIn):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    for attr, value in payload.dict().items():
        setattr(task, attr, value)
    task.save()
    return task


@router.delete("/tasks/{task_id}")
def delete_task(request, task_id: int):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return {"success": True}


@router.get("/tasks/filter/{status}", response=List[TaskOut])
def filter_tasks(request, status: str):
    tasks = Task.objects.filter(user=request.user, status=status)
    return tasks


@router.get("/tasks/sort/created", response=List[TaskOut])
def sort_tasks_by_created(request):
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    return tasks


@router.get("/tasks/sort/due", response=List[TaskOut])
def sort_tasks_by_due(request):
    tasks = Task.objects.filter(user=request.user).order_by('due_date')
    return tasks
