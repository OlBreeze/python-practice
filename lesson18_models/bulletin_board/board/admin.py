from django.contrib import admin
from .models import Category, Ad, Comment, UserProfile


# Клас для UserProfile
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address')
    search_fields = ('user__username', 'phone_number')
    list_per_page = 20


# Клас для Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'active_ads_count')
    search_fields = ('name', 'description')
    list_per_page = 20
    
    def active_ads_count(self, obj):
        return obj.get_active_ads_count()
    active_ads_count.short_description = 'Активних оголошень'


# Клас для Ad
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'user', 'price', 'is_active', 'created_at')
    list_filter = ('is_active', 'category', 'created_at')
    search_fields = ('title', 'description', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20
    
    fieldsets = (
        ('Основна інформація', {
            'fields': ('title', 'description', 'price', 'category')
        }),
        ('Користувач', {
            'fields': ('user',)
        }),
        ('Статус', {
            'fields': ('is_active',)
        }),
        ('Дати', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# Клас для Comment
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'ad', 'short_content', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'user__username', 'ad__title')
    readonly_fields = ('created_at',)
    list_per_page = 20
    
    def short_content(self, obj):
        if len(obj.content) > 50:
            return f"{obj.content[:50]}..."
        return obj.content
    short_content.short_description = 'Коментар'


# Реєстрація моделей
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Ad, AdAdmin)
admin.site.register(Comment, CommentAdmin)