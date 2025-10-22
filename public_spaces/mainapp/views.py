from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Places


def place_detail(request, pk):
    place = get_object_or_404(Places, pk=pk)

    data = {
        'title': place.title,
        'description': place.description,
        'latitude': place.latitude,
        'longitude': place.longitude,
        'image': request.build_absolute_uri(place.image.url) if place.image else None
    }

    return JsonResponse(
        {'data': data},
        json_dumps_params={
            'ensure_ascii': False,  # чтобы кириллица не экранировалась
            'indent': 4  # чтобы JSON был "красивым"
        }
    )
