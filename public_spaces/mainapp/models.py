from django.db import models
from django.utils.text import slugify
from django.utils.html import format_html


class Places(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    latitude = models.FloatField(verbose_name='Широта')
    longitude = models.FloatField(verbose_name='Долгота')
    image = models.ImageField(upload_to='places/', blank=True, null=True, verbose_name='Главное фото')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        db_table = 'public_spaces'
        verbose_name_plural = 'Общественные пространства'
        verbose_name = 'общественное пространство'
        ordering = ['title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class PlaceImage(models.Model):
    place = models.ForeignKey(
        'Places',
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Локация'
    )
    image = models.ImageField(upload_to='places/gallery/', verbose_name='Фотография')
    caption = models.CharField(max_length=200, blank=True, verbose_name='Подпись к фото')
    order = models.PositiveIntegerField(default=0, null=False, db_index=True)

    class Meta:
        verbose_name = 'фотография'
        verbose_name_plural = 'Фотографии'
        ordering = ['order']

    def __str__(self):
        return f'Фото для {self.place.title}'

    def image_tag(self):
        if self.image:
            return format_html('<img src="{}" style="width:100px; height:auto; border-radius:5px;" />', self.image.url)
        return "(Нет изображения)"

    image_tag.short_description = 'Превью'
