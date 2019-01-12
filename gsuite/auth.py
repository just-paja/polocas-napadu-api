from django.contrib.auth import get_user_model
from admin_sso.default_settings import ASSIGNMENT_MATCH
from admin_sso.models import Assignment


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
            user = cls(
                email=sso_email,
                username=sso_email,
                is_staff=True,
            )
            user.save()
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
