# Generated by Django 2.2 on 2019-04-15 00:30

from django.db import migrations
import fields.description


class Migration(migrations.Migration):

    dependencies = [
        ("locations", "0002_auto_20190112_1615"),
    ]

    operations = [
        migrations.AlterField(
            model_name="location",
            name="description",
            field=fields.description.DescriptionField(
                help_text="nameDescriptionText", verbose_name="Description"
            ),
        ),
        migrations.AlterField(
            model_name="locationphoto",
            name="description",
            field=fields.description.DescriptionField(
                default=None,
                help_text="nameDescriptionText",
                verbose_name="Description",
            ),
            preserve_default=False,
        ),
    ]
