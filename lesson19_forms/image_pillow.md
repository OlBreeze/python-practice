# 🖼️ ВИКОРИСТАННЯ PILLOW ДЛЯ ОБРОБКИ ЗОБРАЖЕНЬ

## Що таке Pillow?

**Pillow** - це бібліотека Python для роботи з зображеннями. Це форк оригінальної бібліотеки PIL (Python Imaging Library).

---

## 📦 Встановлення

```bash
pip install Pillow --break-system-packages
```

Версія в проекті: **Pillow 11.3.0**

---

## 🎯 Використання в проекті

### 1. Django ImageField

Django використовує Pillow для роботи з `ImageField`:

```python
avatar = models.ImageField(
    upload_to='avatars/',
    blank=True,
    null=True,
    validators=[validate_image_size],
    verbose_name="Аватар"
)
```

**Що робить Pillow:**
- ✅ Перевіряє, чи файл є зображенням
- ✅ Валідує формат (JPG, PNG, GIF, тощо)
- ✅ Дозволяє обробляти зображення

---

### 2. Валідація розміру файлу

```python
def validate_image_size(image):
    """Валідація розміру зображення (максимум 2 МБ)"""
    file_size = image.size
    limit_mb = 2
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError(f"Максимальний розмір файлу {limit_mb} МБ")
```

**Застосування:**
- Обмежує розмір файлу до 2 МБ
- Викликає помилку валідації при перевищенні

---

### 3. Автоматична оптимізація зображень ⭐ НОВА ФУНКЦІЯ

```python
from PIL import Image
from io import BytesIO

def save(self, *args, **kwargs):
    """Автоматична оптимізація зображення при збереженні"""
    if self.avatar:
        img = Image.open(self.avatar)
        
        # 1. Конвертація RGBA → RGB
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1])
            img = background
        
        # 2. Зміна розміру (макс. 800x800)
        max_size = (800, 800)
        if img.height > max_size[0] or img.width > max_size[1]:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # 3. Оптимізація якості
        output = BytesIO()
        img.save(output, format='JPEG', quality=85, optimize=True)
        
    super().save(*args, **kwargs)
```

**Що робить оптимізація:**

#### 🎨 Конвертація формату
- PNG з прозорістю → JPEG з білим фоном
- GIF → JPEG
- Всі формати → JPEG (оптимальний для фото)

#### 📐 Зміна розміру
- Максимальний розмір: **800x800 пікселів**
- Зберігає пропорції (aspect ratio)
- Використовує LANCZOS для якісного масштабування

#### ⚡ Стиснення
- Якість: **85%** (оптимальний баланс)
- Оптимізація: **увімкнена** (зменшує розмір файлу)
- Формат: **JPEG** (найкраще стиснення)

---

## 📊 Переваги використання Pillow

### До оптимізації:
```
Завантажено: photo.png (3.5 МБ, 4000x3000)
↓
Збережено: photo.png (3.5 МБ, 4000x3000)
```

### Після оптимізації:
```
Завантажено: photo.png (3.5 МБ, 4000x3000)
↓ Pillow обробка
Збережено: photo.jpg (150 КБ, 800x600)
```

**Економія:** 95% розміру! 🎉

---

## 🔧 Налаштування оптимізації

### Змінити максимальний розмір:

```python
# В models.py, метод save()
max_size = (1200, 1200)  # Замість (800, 800)
```

### Змінити якість:

```python
# В models.py, метод save()
img.save(output, format='JPEG', quality=90, optimize=True)  # 90 замість 85
```

**Рекомендації:**
- `quality=60-70` - низька якість, маленький розмір
- `quality=75-85` - оптимальний баланс ✅
- `quality=90-95` - висока якість, більший розмір
- `quality=100` - максимальна якість, дуже великий розмір

### Залишити оригінальний формат:

```python
# Визначити формат з оригінального файлу
format = img.format or 'JPEG'
img.save(output, format=format, quality=85, optimize=True)
```

---

## 🎨 Додаткові можливості Pillow

### Створення мініатюр:

```python
from PIL import Image

def create_thumbnail(image_path, size=(150, 150)):
    img = Image.open(image_path)
    img.thumbnail(size, Image.Resampling.LANCZOS)
    img.save(f"thumb_{image_path}")
```

### Додавання водяних знаків:

```python
from PIL import Image, ImageDraw, ImageFont

def add_watermark(image_path, text="©"):
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 36)
    draw.text((10, 10), text, fill=(255, 255, 255), font=font)
    img.save(f"watermarked_{image_path}")
```

### Обрізка зображення:

```python
from PIL import Image

def crop_center(image_path, size=(300, 300)):
    img = Image.open(image_path)
    width, height = img.size
    left = (width - size[0]) / 2
    top = (height - size[1]) / 2
    right = (width + size[0]) / 2
    bottom = (height + size[1]) / 2
    img = img.crop((left, top, right, bottom))
    img.save(f"cropped_{image_path}")
```

### Фільтри та ефекти:

```python
from PIL import Image, ImageFilter

def apply_filters(image_path):
    img = Image.open(image_path)
    
    # Розмиття
    blurred = img.filter(ImageFilter.BLUR)
    
    # Чорно-біле
    grayscale = img.convert('L')
    
    # Різкість
    sharp = img.filter(ImageFilter.SHARPEN)
    
    return blurred, grayscale, sharp
```

---

## 🧪 Тестування Pillow

### Перевірка роботи оптимізації:

```python
# Django shell
python manage.py shell

from django.contrib.auth.models import User
from accounts.models import UserProfile
from django.core.files import File

# Завантажити тестове зображення
user = User.objects.get(username='admin')
with open('test_large_image.png', 'rb') as f:
    user.profile.avatar.save('test.png', File(f))

# Перевірити розмір
print(f"Розмір файлу: {user.profile.avatar.size} байт")

# Відкрити з Pillow
from PIL import Image
img = Image.open(user.profile.avatar.path)
print(f"Розміри: {img.size}")
print(f"Формат: {img.format}")
```

---

## 📝 Підтримувані формати

### Читання (вхідні):
- ✅ JPEG/JPG
- ✅ PNG (з прозорістю)
- ✅ GIF
- ✅ BMP
- ✅ TIFF
- ✅ WebP
- ✅ ICO

### Збереження (вихідні):
- ✅ JPEG (використовується в проекті)
- ✅ PNG
- ✅ GIF
- ✅ BMP
- ✅ WebP

---

## ⚠️ Важливі примітки

### 1. Вимога до встановлення

**Pillow ОБОВ'ЯЗКОВИЙ** для роботи ImageField в Django!

Без Pillow отримаєте помилку:
```
SystemError: The _imaging extension was not built.
```

### 2. Безпека

Pillow автоматично перевіряє:
- ✅ Чи файл є зображенням
- ✅ Чи не пошкоджений файл
- ✅ Чи не містить зловмисний код

### 3. Продуктивність

- Обробка 1 зображення: ~0.5-2 секунди
- Залежить від розміру оригіналу
- Відбувається асинхронно при збереженні

---

## 🚀 Рекомендації

### Для веб-додатків:

1. **Завжди оптимізуйте зображення** ✅
   - Зменшує навантаження на сервер
   - Прискорює завантаження сторінок
   - Економить місце на диску

2. **Встановіть обмеження:**
   - Максимальний розмір файлу: 2 МБ
   - Максимальні розміри: 800x800
   - Формат: JPEG для фото, PNG для графіки

3. **Створюйте мініатюри:**
   - Для списків користувачів
   - Для галерей
   - Для превью

---

## 📚 Додаткові ресурси

- **Офіційна документація:** https://pillow.readthedocs.io/
- **GitHub:** https://github.com/python-pillow/Pillow
- **Django ImageField:** https://docs.djangoproject.com/en/5.2/ref/models/fields/#imagefield

---

## 💡 Поради

### Проблема: Зображення перевертаються

```python
from PIL import Image, ExifTags

# Виправити орієнтацію з EXIF
def fix_orientation(img):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(img._getexif().items())
        if exif[orientation] == 3:
            img = img.rotate(180, expand=True)
        elif exif[orientation] == 6:
            img = img.rotate(270, expand=True)
        elif exif[orientation] == 8:
            img = img.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        pass
    return img
```

### Проблема: Велике використання пам'яті

```python
# Обробляти по частинах для великих зображень
from PIL import Image
Image.MAX_IMAGE_PIXELS = 200000000  # Збільшити ліміт
```

---

**Pillow робить роботу з зображеннями простою та ефективною! 🎨**
---
```python

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


def validate_image_size(image):
    """Валідація розміру зображення (максимум 2 МБ)"""
    file_size = image.size
    limit_mb = 2
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError(f"Максимальний розмір файлу {limit_mb} МБ")


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True, verbose_name="Біографія")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата народження")
    location = models.CharField(max_length=100, blank=True, verbose_name="Місце проживання")
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        validators=[validate_image_size],
        verbose_name="Аватар"
    )

    class Meta:
        verbose_name = "Профіль користувача"
        verbose_name_plural = "Профілі користувачів"

    def __str__(self):
        return f"Профіль {self.user.username}"
    
    def save(self, *args, **kwargs):
        """Автоматична оптимізація зображення при збереженні"""
        if self.avatar:
            # Відкриваємо зображення з Pillow
            img = Image.open(self.avatar)
            
            # Конвертуємо RGBA в RGB (для PNG з прозорістю)
            if img.mode in ('RGBA', 'LA', 'P'):
                # Створюємо білий фон
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            # Обмежуємо максимальний розмір (наприклад, 800x800)
            max_size = (800, 800)
            if img.height > max_size[0] or img.width > max_size[1]:
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Зберігаємо оптимізоване зображення
            output = BytesIO()
            img.save(output, format='JPEG', quality=85, optimize=True)
            output.seek(0)
            
            # Оновлюємо файл
            self.avatar = InMemoryUploadedFile(
                output, 'ImageField',
                f"{self.avatar.name.split('.')[0]}.jpg",
                'image/jpeg',
                sys.getsizeof(output), None
            )
        
        super().save(*args, **kwargs)
```
