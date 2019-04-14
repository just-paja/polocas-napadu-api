"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from api_admin.admin import ADMIN_SITE
from gsuite.views import gauth
from shows import urls as shows
from theatre_sports import urls as theatre_sports


urlpatterns = [
    path('admin/', ADMIN_SITE.urls),
    path('graphql', csrf_exempt(GraphQLView.as_view(graphiql=settings.DEBUG)), name='api_public'),
    path('shows/', include(shows.urlpatterns)),
    path('theatre-sports/', include(theatre_sports.urlpatterns)),
    path('', gauth),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
