from django.shortcuts import render
from mainapp.models import Places


def start_view(request):
    places_data = []

    for place in Places.objects.all():
        gallery = [
            {
                'image': request.build_absolute_uri(img.image.url),
            }
            for img in place.images.all() if img.image
        ]

        places_data.append({
            'title': place.title,
            'description': place.description,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'image': request.build_absolute_uri(place.image.url) if place.image else None,
            'gallery': gallery
        })
    return render(request, 'start.html', {'places': places_data})
