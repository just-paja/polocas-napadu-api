from django.db import migrations, models
import django_extensions.db.fields
import fields.name
import fields.weight


class Migration(migrations.Migration):
    dependencies = [
        ('events', '0007_update_content_types'),
    ]

    state_operations = [
        migrations.CreateModel(
            name="EventParticipant",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                (
                    "show",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE,
                        related_name='eventParticipants',
                        to='events.Event',
                        verbose_name='Show',
                    ),
                ),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE,
                        related_name='eventsParticipated',
                        to='profiles.Profile',
                        verbose_name='Profile',
                    ),
                ),
                (
                    "role",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE,
                        related_name='eventParticipants',
                        to='events.ParticipantRole',
                        verbose_name='Role',
                    ),
                ),
            ],
            options={
                "verbose_name": "Event participant",
                "verbose_name_plural": "Event participants"
            },
        ),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=state_operations,
        )
    ]
