# Generated by Django 2.2.10 on 2020-03-02 17:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0003_auto_20200302_1719'),
    ]

    operations = [
        migrations.RenameField(
            model_name='statement',
            old_name='counter_party',
            new_name='counterparty',
        ),
    ]
