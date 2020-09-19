from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_event'),
        ('theatre_sports', '0022_regenerate_slugs'),
        ('shows', '0031_delete_shows'),
    ]

    state_operations = [
        migrations.AlterField(
            model_name='Match',
            name='show',
            field=models.OneToOneField(
                on_delete=models.deletion.CASCADE,
                related_name='match',
                to='events.Event',
            )
        ),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(state_operations=state_operations)
    ]
