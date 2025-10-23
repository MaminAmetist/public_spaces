from ckeditor.fields import RichTextField
from django.db import models
from django.utils.html import format_html
from django.db.models.fields.files import ImageFieldFile


class Places(models.Model):
    """Создает БД мест для посещения"""
    title = models.CharField(max_length=100, verbose_name='Название')
    description = RichTextField(verbose_name='Описание')
    latitude = models.FloatField(verbose_name='Широта')
    longitude = models.FloatField(verbose_name='Долгота')
    image = models.ImageField(upload_to='places/', blank=True, null=True,
                              verbose_name='Главное фото')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'public_spaces'
        verbose_name_plural = 'Общественные пространства'
        verbose_name = 'общественное пространство'
        ordering = ['title']

    def __str__(self):
        return self.title


class PlaceImage(models.Model):
    """Создает БД галереи"""
    place = models.ForeignKey(
        'Places',
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Локация'
    )
    image = models.ImageField(upload_to='places/gallery/', verbose_name='Фотография')
    order = models.PositiveIntegerField(default=0, null=False, db_index=True)

    class Meta:
        verbose_name = 'фотография'
        verbose_name_plural = 'Фотографии'
        ordering = ['order']

    def __str__(self):
        return f'Фото для {self.place.title}'

    def image_tag(self):
        image: ImageFieldFile = self.image
        if image:
            return format_html(f'<img src="{image.url}" style="width:100px;'
                               f' height:auto; border-radius:5px;" />')
        return "(Нет изображения)"

    image_tag.short_description = 'Превью'
