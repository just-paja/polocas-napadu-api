from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0002_auto_20191029_0901'),
        ('shows', '0031_delete_shows'),
    ]

    state_operations = [
        migrations.AlterField(
            model_name='Reservation',
            name='show',
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE,
                related_name='reservations',
                to='events.Event',
            )
        ),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(state_operations=state_operations)
    ]
