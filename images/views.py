from django.http import Http404
from django.conf import settings
from django.shortcuts import redirect
from sorl.thumbnail import get_thumbnail

FORMATS = ['jpeg', 'webp']


def thumbnail(request, image_size, image_format):
    image = request.GET.get('image', None)
    size_params = settings.THUMBNAILS.get(image_size, None)
    if not image or not size_params and image_format in FORMATS:
        raise Http404
    thumb = get_thumbnail(
        image,
        '%sx%s' % (size_params.get('width'), size_params.get('height')),
        crop=size_params.get('crop', None),
        quality=80,
        format=image_format.upper(),
    )
    return redirect(thumb.url, permanent=True)
