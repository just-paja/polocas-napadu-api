from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.http import Http404

def gauth(req):
    if settings.DJANGO_ADMIN_SSO:
        return redirect(reverse('admin:admin_sso_assignment_start'))
    raise Http404
