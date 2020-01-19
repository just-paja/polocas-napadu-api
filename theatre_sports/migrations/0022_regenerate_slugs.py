from django.db import migrations


def save_all_foul_types(apps, schema_editor):
    FoulType = apps.get_model("theatre_sports", "FoulType")
    db_alias = schema_editor.connection.alias
    objects = FoulType.objects.using(db_alias).all()
    for foul_type in objects:
        foul_type.save()


class Migration(migrations.Migration):

    dependencies = [
        ("theatre_sports", "0022_foultype_slug"),
    ]

    operations = [
        migrations.RunPython(save_all_foul_types, save_all_foul_types),
    ]
