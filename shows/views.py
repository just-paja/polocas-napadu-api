from django.http import Http404, HttpResponse
from qrcode import make

from .models import Show

def show_inspiration_qr(request, show_id):
    try:
        show = Show.objects.get(pk=show_id)
    except Show.DoesNotExist:
        raise Http404
    image = make(show.get_inspiration_url())
    response = HttpResponse(content_type='image/png')
    image.save(response, 'png')
    return response
