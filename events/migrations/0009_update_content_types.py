from django.db import migrations, models
import django_extensions.db.fields
import fields.name
import fields.weight

def update_content_types(apps, schema_editor):
    content_type = apps.get_model('contenttypes', 'ContentType')
    db_alias = schema_editor.connection.alias
    query = content_type.objects.using(db_alias).filter(app_label='shows', model='ShowTicketPrice')
    query.update(app_label='events', model='EventTicketPrice')

def update_content_types_reverse(apps, schema_editor):
    content_type = apps.get_model('contenttypes', 'ContentType')
    db_alias = schema_editor.connection.alias
    query = content_type.objects.using(db_alias).filter(app_label='events', model='EventTicketPrice')
    query.update(app_label='shows', model='ShowTicketPrice')


class Migration(migrations.Migration):
    dependencies = [
        ('events', '0008_event_participant'),
        ('shows', '0041_rename_show_ticket_price_table'),
        ('theatre_sports', '0025_retarget_event_participant'),
        ('games', '0010_retarget_event_participant'),
    ]

    database_operations = [
        migrations.RunPython(
            update_content_types,
            update_content_types_reverse,
        ),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=database_operations,
        )
    ]
