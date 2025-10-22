from django.contrib import admin
from .models import Places


@admin.register(Places)
class PlacesAdmin(admin.ModelAdmin):
    list_display = ('title', 'latitude', 'longitude', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'image')
        }),
        ('Геолокация', {
            'fields': ('latitude', 'longitude'),
            'description': 'Введите координаты места (широту и долготу)'
        }),
        ('Дополнительно', {
            'fields': ('slug', 'created_at', 'updated_at'),
        }),
    )
