# Generated by Django 2.2 on 2019-04-15 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bands', '0004_auto_20190415_0030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bandphoto',
            name='description',
            field=models.TextField(),
        ),
    ]