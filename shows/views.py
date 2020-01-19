from django.urls import reverse
from django.conf import settings
from django.http import Http404, HttpResponse
from qrcode import make

from .models import Show


def get_inspiration_url(request, show):
    api_url = request.build_absolute_uri(reverse("api_public"))
    return "%s?apiUrl=%s#/match/%s" % (
        settings.APP_INSPIRATIONS_URL,
        api_url,
        show.match.pk,
    )


def show_inspiration_qr(request, show_id):
    try:
        show = Show.objects.get(pk=show_id)
    except Show.DoesNotExist:
        raise Http404
    if show.match:
        inspiration_url = get_inspiration_url(request, show)
    else:
        inspiration_url = "https://tema.polocas-napadu.cz"

    image = make(inspiration_url)
    response = HttpResponse(content_type="image/png")
    image.save(response, "png")
    return response
