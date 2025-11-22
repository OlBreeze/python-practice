from ninja import Router
from django.shortcuts import get_object_or_404
from typing import List
from .models import *
from .schemas import *

router = Router()


@router.get("/servers", response=List[ServerOut])
def list_servers(request):
    return Server.objects.all()


@router.post("/servers", response=ServerOut)
def create_server(request, payload: ServerIn):
    server = Server.objects.create(**payload.dict())
    return server


@router.get("/servers/{server_id}", response=ServerOut)
def get_server(request, server_id: int):
    return get_object_or_404(Server, id=server_id)


@router.put("/servers/{server_id}", response=ServerOut)
def update_server(request, server_id: int, payload: ServerIn):
    server = get_object_or_404(Server, id=server_id)
    for attr, value in payload.dict().items():
        setattr(server, attr, value)
    server.save()
    return server


@router.delete("/servers/{server_id}")
def delete_server(request, server_id: int):
    server = get_object_or_404(Server, id=server_id)
    server.delete()
    return {"success": True}


@router.post("/servers/{server_id}/metrics", response=MetricOut)
def add_metric(request, server_id: int, payload: MetricIn):
    server = get_object_or_404(Server, id=server_id)
    metric = ServerMetric.objects.create(server=server, **payload.dict())

    if metric.cpu_usage > 90 or metric.memory_usage > 90:
        Alert.objects.create(
            server=server,
            message=f"Критичне навантаження на сервер {server.name}",
            is_critical=True
        )

    return metric


@router.get("/servers/{server_id}/metrics", response=List[MetricOut])
def get_metrics(request, server_id: int):
    return ServerMetric.objects.filter(server_id=server_id)
