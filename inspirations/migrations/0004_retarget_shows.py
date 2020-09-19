from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspirations', '0003_auto_20190126_1402'),
        ('shows', '0031_delete_shows'),
    ]

    state_operations = [
        migrations.AlterField(
            model_name='Inspiration',
            name='show',
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE,
                related_name='inspirations',
                to='events.Event',
            )
        ),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(state_operations=state_operations)
    ]
