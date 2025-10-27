## 📝 Реєстрація моделей в адмін-панелі  - **код у файлі `admin.py`**.

### Спосіб 1: Простий (декоратор)

```python
from django.contrib import admin
from .models import Category, Ad, Comment, UserProfile

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'is_active')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'ad', 'created_at')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')
```

### Спосіб 2: Класичний

```python
from django.contrib import admin
from .models import Category, Ad, Comment, UserProfile

admin.site.register(Category)
admin.site.register(Ad)
admin.site.register(Comment)
admin.site.register(UserProfile)
```
---
## 🔑 Ключові атрибути ModelAdmin

### Основні налаштування:

```python
class MyModelAdmin(admin.ModelAdmin):
    # Поля для відображення в списку
    list_display = ('field1', 'field2', 'field3')
    
    # Поля для пошуку
    search_fields = ('field1', 'field2')
    
    # Фільтри в бічній панелі
    list_filter = ('field1', 'field2')
    
    # Поля тільки для читання
    readonly_fields = ('created_at', 'updated_at')
    
    # Кількість записів на сторінці
    list_per_page = 25
    
    # Поля для редагування прямо в списку
    list_editable = ('is_active',)
    
    # Сортування за замовчуванням
    ordering = ('-created_at',)
    
    # Дата ієрархія
    date_hierarchy = 'created_at'
```

---

## 🔍 Приклади search_fields

### Пошук у пов'язаних моделях:

```python
# Пошук за username користувача (через ForeignKey)
search_fields = ('user__username',)

# Пошук за email користувача
search_fields = ('user__email',)

# Пошук за назвою категорії
search_fields = ('category__name',)

# Пошук за декількома полями
search_fields = ('title', 'description', 'user__username', 'user__email')

# Точний пошук (=)
search_fields = ('=id',)

# Пошук з початку рядка (^)
search_fields = ('^title',)
```

---

## 📊 Порівняння способів

### Декоратор (сучасний):
```python
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)
```

**Плюси:** 
- ✅ Компактніше
- ✅ Сучасніше
- ✅ Менше коду

### Класичний:
```python
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)

admin.site.register(Category, CategoryAdmin)
```

**Плюси:**
- ✅ Більш явне
- ✅ Легше для початківців
- ✅ Можна реєструвати одну модель кілька разів (рідкісний випадок)

---

**Висновок:** У класичному способі потрібно:
1. Створити клас `ModelNameAdmin(admin.ModelAdmin)`
2. Додати атрибути (`search_fields`, `list_display`, тощо)
3. Зареєструвати: `admin.site.register(ModelName, ModelNameAdmin)`