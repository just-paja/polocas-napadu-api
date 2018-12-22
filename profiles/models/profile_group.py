from django.db.models import BooleanField, CharField, Model

from fields import NameMixin

class ProfileGroup(NameMixin):
    public = BooleanField(default=False)
