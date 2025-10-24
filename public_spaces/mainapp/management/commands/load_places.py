import os
import json
import requests
from urllib.parse import urlparse
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from mainapp.models import Places, PlaceImage


class Command(BaseCommand):
    help = "Загружает одно место из JSON-файла или несколько мест из index.json"

    def add_arguments(self, parser):
        parser.add_argument(
            'path',
            type=str,
            help='Путь или URL к JSON-файлу с местом или index.json со списком мест'
        )

    def handle(self, *args, **options):
        path = options['path']

        # Загружаем JSON из URL или файла
        data = self.load_json(path)

        # Если это список — рекурсивно обрабатываем каждый элемент
        if isinstance(data, list):
            self.stdout.write(f'Читаем список мест из {path}')
            for item in data:
                if item.startswith(('http://', 'https://')):
                    self.handle_single_place(item)
                else:
                    abs_path = os.path.abspath(item)
                    if not os.path.exists(abs_path):
                        self.stdout.write(self.style.WARNING(f'Файл {abs_path} не найден, пропускаем'))
                        continue
                    self.handle_single_place(abs_path)
            self.stdout.write(self.style.SUCCESS('Все места успешно загружены'))
        else:
            self.handle_single_place(path)

    def load_json(self, source):
        """Загружает JSON из URL или локального файла"""
        try:
            if source.startswith(('http://', 'https://')):
                response = requests.get(source)
                response.raise_for_status()
                return response.json()
            else:
                with open(source, encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            raise CommandError(f'Ошибка при чтении {source}: {e}')

    def handle_single_place(self, source):
        """Загружает одно место из JSON"""
        data = self.load_json(source)
        title = data.get('title')

        if not title:
            raise CommandError(f"В файле {source} отсутствует поле 'title'")

        place, created = Places.objects.get_or_create(title=title, defaults={
            'description': data.get('description', ''),
            'latitude': data.get('latitude'),
            'longitude': data.get('longitude'),
        })

        if not created:
            self.stdout.write(f'Место "{title}" уже существует, обновляем данные')
            place.description = data.get('description', place.description)
            place.latitude = data.get('latitude', place.latitude)
            place.longitude = data.get('longitude', place.longitude)
            place.save()

        # Основное изображение
        image_url = data.get('image')
        if image_url:
            try:
                img_resp = requests.get(image_url)
                img_resp.raise_for_status()
                filename = os.path.basename(urlparse(image_url).path)
                place.image.save(filename, ContentFile(img_resp.content), save=True)
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Не удалось загрузить изображение: {e}'))

        # Галерея
        gallery = data.get('gallery', [])
        for item in gallery:
            img_url = item.get('image') if isinstance(item, dict) else item
            if not img_url:
                continue
            try:
                img_resp = requests.get(img_url)
                img_resp.raise_for_status()
                filename = os.path.basename(urlparse(img_url).path)
                image_file = ContentFile(img_resp.content)
                PlaceImage.objects.create(place=place, image=image_file)
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Не удалось добавить фото: {e}'))

        self.stdout.write(self.style.SUCCESS(f'Место "{title}" успешно загружено'))
