from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shows', '0041_rename_show_ticket_price_table'),
    ]

    state_operations = [
        migrations.DeleteModel('ShowTicketPrice'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(state_operations=state_operations)
    ]
