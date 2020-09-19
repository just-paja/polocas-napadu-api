from django.db import migrations, models
import django_extensions.db.fields
import fields.name
import fields.weight

def update_content_types(apps, schema_editor):
    content_type = apps.get_model('contenttypes', 'ContentType')
    db_alias = schema_editor.connection.alias
    query = content_type.objects.using(db_alias).filter(app_label='shows', model='ShowRole')
    query.update(app_label='events', model='ParticipantRole')

def update_content_types_reverse(apps, schema_editor):
    content_type = apps.get_model('contenttypes', 'ContentType')
    db_alias = schema_editor.connection.alias
    query = content_type.objects.using(db_alias).filter(app_label='events', model='ParticipantRole')
    query.update(app_label='shows', model='ShowRole')


class Migration(migrations.Migration):
    dependencies = [
        ('events', '0001_initial'),
        ('shows', '0027_auto_20200919_2251'),
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
