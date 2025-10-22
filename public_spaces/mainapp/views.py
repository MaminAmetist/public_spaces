from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Places


def place_detail(request, pk):
    place = get_object_or_404(Places, pk=pk)

    images = [
        request.build_absolute_uri(img.image.url)
        for img in place.images.all()
        if img.image
    ]

    data = {
        'title': place.title,
        'description': place.description,
        'latitude': place.latitude,
        'longitude': place.longitude,
        'image': request.build_absolute_uri(place.image.url) if place.image else None,
        'gallery': images
    }

    return JsonResponse({'data': data}, json_dumps_params={'ensure_ascii': False, 'indent': 4})
