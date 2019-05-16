from django.core.exceptions import ValidationError

class AlreadyClosed(ValidationError):
    pass
