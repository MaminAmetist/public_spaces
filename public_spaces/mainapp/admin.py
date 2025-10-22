from django.contrib import admin
from .models import Places, PlaceImage
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminBase


class PlaceImageInline(SortableInlineAdminMixin, admin.StackedInline):
    model = PlaceImage
    extra = 1
    fields = ('image_tag', 'image', 'caption', 'order')
    readonly_fields = ('image_tag',)
    verbose_name = "фотография"
    verbose_name_plural = "Фотографии локации"


@admin.register(Places)
class PlacesAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ('title', 'latitude', 'longitude', 'created_at', 'updated_at')
    search_fields = ('title',)
    inlines = [PlaceImageInline]
