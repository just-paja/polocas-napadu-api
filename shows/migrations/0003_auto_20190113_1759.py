# Generated by Django 2.2.dev20190104142447 on 2019-01-13 17:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("shows", "0002_auto_20190112_1615"),
    ]

    operations = [
        migrations.RemoveField(model_name="matchscore", name="results",),
        migrations.RemoveField(model_name="matchscore", name="show_band",),
        migrations.DeleteModel(name="MatchResults",),
        migrations.DeleteModel(name="MatchScore",),
    ]
