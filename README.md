# Public Spaces (Общественные пространства)

Интерактивная карта Москвы с метками публичных мест для посещения.

## Особенности

- Отображение мест на карте с сайдбаром.
- Поддержка нескольких изображений на каждую локацию.
- WYSIWYG-редактор для описания мест в админке.
- Сортировка изображений в админке drag-and-drop.
- API для получения данных о местах в формате JSON.

## Структура проекта
```bash
    public_spaces/
    ├── public_spaces/            
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── settings.py           
    │   ├── urls.py               
    │   ├── views.py              # Представления для карты
    │   └── wsgi.py
    │
    ├── mainapp/                  # Основное приложение проекта
    │   ├── migrations/           
    │   ├── admin.py              # Настройка админ-панели
    │   ├── apps.py
    │   ├── models.py             # Модели Places и PlaceImage
    │   ├── tests.py
    │   ├── urls.py              
    │   └── views.py              # Представления для API
    │
    ├── manage.py                 
    ├── db.sqlite3                
    ├── .env                      # Файл переменных окружения 
    ├── requirements.txt          
    ├── templates/                # HTML-шаблоны
    └── media/                    # Загруженные изображения
  
```

## Установка

Клонировать репозиторий:
```bash
    git clone https://github.com/MaminAmetist/public_spaces.git
    cd public_spaces
   ```

Создать виртуальное окружение и активировать его:

```bash
    python -m venv venv
    venv\Scripts\activate       # Windows
    # source venv/bin/activate  # Linux/Mac
```

Установить зависимости:

```bash
pip install -r requirements.txt
```

Создать файл .env в корне проекта с настройками:
```bash
    SECRET_KEY=your-secret-key
    DEBUG=True
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'yourusername.pythonanywhere.com']
    MEDIA_ROOT=C:\path\to\media
```

Применить миграции:

```bash
  python manage.py migrate
```

Создать суперпользователя:

```bash
  python manage.py createsuperuser
```

Запустить настройки static файлов:

```bash
  python manage.py collectstatic
```
## Использование

Админка: https://maminametist.pythonanywhere.com/admin/

Добавление и редактирование мест, загрузка галерей.

Drag-and-drop для сортировки фотографий.

Главная страница: https://maminametist.pythonanywhere.com/

Интерактивная карта с местами и сайдбаром.

API: https://maminametist.pythonanywhere.com/places/<id>/ 

Возвращает JSON с данными о месте.
