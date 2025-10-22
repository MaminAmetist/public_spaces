from django.contrib import admin
from .models import Places, PlaceImage


class PlaceImageInline(admin.TabularInline):
    model = PlaceImage
    extra = 1
    fields = ('image', 'image_tag', 'caption',)
    readonly_fields = ('image_tag',)
    verbose_name = "фотография"
    verbose_name_plural = "Фотографии локации"


@admin.register(Places)
class PlacesAdmin(admin.ModelAdmin):
    list_display = ('title', 'latitude', 'longitude', 'created_at', 'updated_at')
    search_fields = ('title',)
    inlines = [PlaceImageInline]
