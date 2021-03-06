# Generated by Django 2.2.16 on 2020-09-20 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0009_retarget_event'),
        ('events', '0008_event_participant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='GameActor',
            name='participant',
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE,
                to='events.EventParticipant',
            )
        ),
    ]
