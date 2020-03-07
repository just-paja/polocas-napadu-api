from django.utils.timezone import now
from django.conf import settings
from django.core import mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _
from django.db.models import (
    BooleanField,
    DateTimeField,
    EmailField,
    CharField,
    PositiveSmallIntegerField,
    TextField,
)

from django_extensions.db.models import TimeStampedModel

EMAIL_FORMAT_TEXT = 1
EMAIL_FORMAT_HTML = 2

EMAIL_FORMAT_CHOICES = (
    (EMAIL_FORMAT_TEXT, _('Text')),
    (EMAIL_FORMAT_HTML, _('HTML')),
)

class EmailNotification(TimeStampedModel):
    class Meta:
        verbose_name = _("Email notification")
        verbose_name_plural = _("Email notifications")

    key = CharField(
        max_length=255,
        verbose_name=_('Notification key'),
        help_text=_('Key specific to the notification source'),
    )
    subject = CharField(
        help_text=_('Few words to describe contents of the e-mail'),
        max_length=255,
        verbose_name=_('Subject'),
    )
    sender_name = CharField(
        default=settings.EMAIL_ROBOT_NAME,
        help_text=_('Name that will be displayed next to sender e-mail address'),
        max_length=255,
        verbose_name=_('Sender name'),
    )
    sender_email = EmailField(
        default=settings.EMAIL_ROBOT_ADDR,
        help_text=_('E-mail address of the sender'),
        verbose_name=_('Sender email'),
    )
    sender_appends_org = BooleanField(
        default=True,
        verbose_name=_('Append organization to sender'),
        help_text=_(
            'Organization name will be appended to the sender name, \
            resulting in things like "Karel from %s"' % settings.ORGANIZATION_NAME
        ),
    )
    recipient_email = EmailField(
        help_text=_('E-mail address of the recipient'),
        verbose_name=_('Recipient email'),
    )
    scheduled_on = DateTimeField(
        blank=False,
        help_text=_('System will proceed and send this e-mail after this datetime.'),
        null=True,
        verbose_name=_('Scheduled on'),
    )
    sent_on = DateTimeField(
        blank=True,
        help_text=_('On this date and time, the e-mail was sent.'),
        null=True,
        verbose_name=_('Sent on'),
    )
    ready = BooleanField(
        default=False,
        help_text=_('Ready e-mails will be sent at first valid opportunity after scheduled date'),
        verbose_name=_('Ready to send'),
    )
    content_format = PositiveSmallIntegerField(
        choices=EMAIL_FORMAT_CHOICES,
        verbose_name=_('Format'),
    )
    content = TextField(
    verbose_name=_('Content'),
        help_text=_(
            'Enter formatted e-mail content. The text version will be auto \
            generated for HTML e-mails'
        ),
    )

    @classmethod
    def schedule(
        cls,
        *,
        date,
        content_format=EMAIL_FORMAT_HTML,
        key,
        recipient_email,
        subject,
        template,
        **kwargs
    ):
        context = {**kwargs}
        content = render_to_string(template, {'context': context})
        notification = cls(
            content=content,
            content_format=content_format,
            key=key,
            recipient_email=recipient_email,
            scheduled_on=date,
        )
        notification.save()

    def __str__(self):
        return '%s to %s (#%s)' % (self.subject, self.recipient_email, self.pk)

    def send(self):
        if self.content_format == EMAIL_FORMAT_HTML:
            html_message = self.content
            plain_message = strip_tags(self.content)
        else:
            html_message = None
            plain_message = self.content

        sender_name = (
            _('%(person)s from %(organization)s' % ({
                'person': self.sender_name,
                'organization': settings.ORGANIZATION_NAME
            }))
            if self.sender_appends_org
            else self.sender_name
        )
        from_email = '%s <%s>' % (sender_name, self.sender_email)
        mail.send_mail(
            self.subject,
            plain_message,
            from_email,
            [self.recipient_email],
            html_message=html_message,
        )
        self.sent_on = now()
        self.save()

    def should_be_sent(self):
        return self.ready and (
            not self.scheduled_on
            or self.scheduled_on < now()
        )

@receiver(post_save, sender=EmailNotification)
def send_email_after_save(sender, instance, **kwargs):
    if instance.ready and not instance.sent_on:
        instance.send()
