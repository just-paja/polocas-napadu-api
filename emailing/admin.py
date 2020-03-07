from django.contrib.admin.utils import flatten_fieldsets

from fields.admin import BaseAdminModel

from .models import EmailNotification


class EmailNotificationAdmin(BaseAdminModel):
    model = EmailNotification
    list_display = (
        "subject",
        "recipient_email",
        "scheduled_on",
        "ready",
        "sent_on",
    )
    search_fields = (
        "content",
        "recipient_email",
        "sender_email",
        "sender_name",
        "subject",
    )
    fieldsets = (
        (None, {"fields": ("key",)}),
        (None, {"fields": ("sender_name", "sender_email", "sender_appends_org"), }),
        (None, {"fields": ("recipient_email",), }),
        (None, {"fields": (
            "subject",
            "content_format",
            "content",
            "ready",
        ), }),
        (None, {"fields": (
            "scheduled_on",
            "sent_on",
        ), }),
    )
    readonly_fields = ('sent_on',)

    def get_readonly_fields(self, request, obj=None):
        if not obj or not obj.sent_on:
            return self.readonly_fields
        if self.fieldsets:
            return flatten_fieldsets(self.fieldsets)
        return list(set(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many]
        ))
