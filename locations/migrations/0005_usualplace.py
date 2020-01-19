# Generated by Django 2.2 on 2019-04-18 09:45

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import fields.description
import fields.name
import fields.visibility


class Migration(migrations.Migration):

    dependencies = [
        ("locations", "0004_auto_20190415_0053"),
    ]

    operations = [
        migrations.CreateModel(
            name="UsualPlace",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "description",
                    fields.description.DescriptionField(
                        help_text="nameDescriptionText", verbose_name="Description"
                    ),
                ),
                (
                    "name",
                    fields.name.NameField(
                        help_text="nameHelpText", max_length=63, verbose_name="Name"
                    ),
                ),
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                (
                    "visibility",
                    fields.visibility.VisibilityField(
                        choices=[(1, "Private"), (2, "Public"), (3, "Deleted")],
                        default=2,
                        help_text="visibilityHelpText",
                        verbose_name="Visibility",
                    ),
                ),
                (
                    "location",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="locations.Location",
                        verbose_name="Location",
                    ),
                ),
            ],
            options={
                "verbose_name": "Usual Place",
                "verbose_name_plural": "Usual Places",
            },
        ),
    ]
