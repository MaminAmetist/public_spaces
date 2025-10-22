from django.shortcuts import render
from mainapp.models import Places


def start_view(request):
    places = Places.objects.all()

    data = []
    for place in places:
        data.append({
            'title': place.title,
            'description': place.description,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'image': request.build_absolute_uri(place.image.url) if place.image else None
        })
    return render(request, 'start.html', {'places': data})
