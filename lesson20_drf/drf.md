
# 🌐 Django REST Framework (DRF)

**DRF** — це потужний і гнучкий набір інструментів для створення Web API в Django.

## 🎯 Основна мета
Спрощення процесу розробки RESTful API, забезпечуючи інструменти для серіалізації, аутентифікації, маршрутизації та багато іншого.

---

## 🧩 Основні концепції та архітектура

### Компоненти:
- **Serializers** — Перетворення даних між Python та JSON/XML.  
- **Views** — Обробка HTTP-запитів та повернення відповідей.  
- **Routers** — Автоматична генерація URL-маршрутів.  
- **Authentication / Authorization** — Механізми безпеки API.  
- **Parsers / Renderers** — Обробка та форматування запитів/відповідей.

### Архітектура:
- DRF базується на Django, використовуючи його моделі та ORM.
- Використовує концепцію *request/response cycle* для обробки HTTP-запитів.

---

## ⚖️ Порівняння з іншими фреймворками

| Фреймворк | Переваги | Недоліки |
|------------|-----------|-----------|
| **Django Ninja** | Швидкий, базується на Pydantic, type hinting | Менше “з коробки” функціоналу |
| **Flask-RESTful** | Простий і легкий | Не має інтеграції з ORM |
| **DRF** | Потужний, гнучкий, інтегрований з Django | Більш “важкий” |

---

## ⚙️ Встановлення та налаштування

```bash
pip install djangorestframework
````

```python
# settings.py
INSTALLED_APPS = [
    # ...
    'rest_framework',
]
```

### Основні налаштування:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}
```

---

## 🧱 Створення першого API View

```python
# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def hello_world(request):
    return Response({'message': 'Hello, world!'})
```

```python
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello_world),
]
```

---

## 🧾 Використання Serializers

### Стандартна серіалізація:

```python
# serializers.py
from rest_framework import serializers
from .models import MyModel

class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'
```

### Валідація:

```python
def validate_field1(self, value):
    if len(value) < 5:
        raise serializers.ValidationError("Field1 must be at least 5 characters long.")
    return value
```

### Гнізда (Nested) та гіперпосилання:

```python
class MyModelSerializer(serializers.ModelSerializer):
    related_model = RelatedModelSerializer()
    related_url = serializers.HyperlinkedIdentityField(view_name='relatedmodel-detail')
```

---

## 📤 CRUD Операції

```python
from rest_framework import generics
from .models import MyModel
from .serializers import MyModelSerializer

class MyModelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer
```

### Обробка помилок:

```python
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

def retrieve(self, request, *args, **kwargs):
    try:
        return super().retrieve(request, *args, **kwargs)
    except NotFound:
        return Response({'error': 'Object not found'}, status=404)
```

---

## 🔁 ViewSets та Routing

```python
from rest_framework import viewsets

class MyModelViewSet(viewsets.ModelViewSet):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer
```

### Автоматичне маршрутування:

```python
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'mymodels', MyModelViewSet)
urlpatterns = router.urls
```

---

## 🔐 Аутентифікація та Авторизація

### Типи аутентифікації:

* **SessionAuthentication**
* **TokenAuthentication**
* **Custom Authentication**

### Кастомна аутентифікація:

```python
from rest_framework import authentication, exceptions

class CustomAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('X-Custom-Token')
        if not token:
            return None
```

### Permissions:

* `IsAuthenticated`
* `IsAdminUser`
* `AllowAny`
* `IsAuthenticatedOrReadOnly`

### Власний дозвіл:

```python
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
```

---

## 🧪 Тестування

* Використовуйте **Postman**, **Insomnia** або **curl**.
* Для юніт-тестів — `APIClient` з DRF.

---

## 📚 Документація API

* **Swagger / OpenAPI** — автоматична генерація документації.
* **drf-spectacular** — бібліотека для створення OpenAPI схем.

---

## 🔢 Версіонування API

```python
urlpatterns = [
    path('v1/mymodels/', views.MyModelList.as_view()),
    path('v2/mymodels/', views.MyModelListV2.as_view()),
]
```

---

## ⚡ Оптимізація та кешування

* **Django-Redis** для кешу.
* **Pagination** для великих наборів даних.
* **CDN** для статичних файлів.
* **Async views** для швидкості.
* **Sentry / Prometheus** для моніторингу.

---

## 🧠 Висновок

Django REST Framework — це **повноцінний інструмент для створення професійних REST API**, який поєднує потужність Django з гнучкістю сучасних веб-технологій.

