from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from admin_sso.default_settings import ASSIGNMENT_MATCH
from admin_sso.models import Assignment

from .groups import GROUP_DEFAULT, GROUP_ADMIN


class GsuiteAuthBackend():
    def get_user(self, user_id):
        cls = get_user_model()
        try:
            return cls.objects.get(pk=user_id)
        except cls.DoesNotExist:
            return None

    def ensure_user_existence(self, sso_email):
        cls = get_user_model()
        try:
            return cls.objects.get(username=sso_email)
        except cls.DoesNotExist:
            group_default = Group.objects.get(name=GROUP_DEFAULT)
            group_admin = Group.objects.get(name=GROUP_ADMIN)
            total_users = cls.objects.count()
            user = cls(
                email=sso_email,
                username=sso_email,
                is_staff=True,
            )
            user.save()
            user.groups.add(group_default)
            if total_users == 0:
                # Assume the first is admin and add him to all groups
                user.groups.add(group_admin)
            return user

    def authenticate(self, request=None, **kwargs):
        sso_email = kwargs.pop('sso_email', None)
        if not sso_email:
            return None

        assignment = Assignment.objects.for_email(sso_email)
        if assignment is None:
            try:
                username, domain = sso_email.split('@')
            except ValueError:
                return None
            user = self.ensure_user_existence(sso_email)
            assignment = Assignment(
                domain=domain,
                user=user,
                username_mode=ASSIGNMENT_MATCH,
                username=username,
            )
            assignment.save()

        return assignment.user
