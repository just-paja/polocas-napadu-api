# Generated by Django 2.2.7 on 2019-11-25 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shows', '0016_showtype_use_fouls'),
    ]

    operations = [
        migrations.AddField(
            model_name='showtype',
            name='use_games',
            field=models.BooleanField(default=False, verbose_name='Use games'),
        ),
    ]