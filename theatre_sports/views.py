from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from graphql_jwt.shortcuts import get_token

from fields import VISIBILITY_PUBLIC
from .models import Match


@staff_member_required
def match_control(request, match_id):
    match = get_object_or_404(Match, pk=match_id, show__visibility=VISIBILITY_PUBLIC)
    token = get_token(request.user)
    return redirect('%s?token=%s#/match/%s' % (
        settings.APP_REFEREE_URL,
        token,
        match.pk
    ))

def match_scoreboard(request, match_id):
    match = get_object_or_404(Match, pk=match_id, show__visibility=VISIBILITY_PUBLIC)
    return redirect('%s#/match/%s' % (
        settings.APP_SCOREBOARD_URL,
        match.pk,
    ))
