# Generated by Django 2.2 on 2019-05-16 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("voting", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="livepollvoting",
            name="closed",
            field=models.BooleanField(default=False, verbose_name="Closed"),
        ),
    ]
