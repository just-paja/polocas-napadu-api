from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0007_regenerate_slugs'),
        ('shows', '0031_delete_shows'),
    ]

    state_operations = [
        migrations.AlterField(
            model_name='Game',
            name='show',
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE,
                related_name='games',
                to='events.Event',
            )
        ),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(state_operations=state_operations)
    ]
