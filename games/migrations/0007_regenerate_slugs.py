from django.db import migrations


def save_all_game_rules(apps, schema_editor):
    GameRules = apps.get_model('games', 'GameRules')
    db_alias = schema_editor.connection.alias
    objects = GameRules.objects.using(db_alias).all()
    for game_rules in objects:
        game_rules.save()


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0006_gamerules_slug'),
    ]

    operations = [
        migrations.RunPython(save_all_game_rules, save_all_game_rules),
    ]
