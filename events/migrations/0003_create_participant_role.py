from django.db import migrations, models
import django_extensions.db.fields
import fields.name
import fields.weight


class Migration(migrations.Migration):
    dependencies = [
        ('events', '0002_update_content_types'),
    ]

    state_operations = [
        migrations.CreateModel(
            name='ParticipantRole',
            fields=[
                ('id', models.AutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID'
                )),
                ('name', fields.name.NameField(
                    help_text='nameHelpText',
                    max_length=63,
                    verbose_name='Name'
                )),
                ('created', django_extensions.db.fields.CreationDateTimeField(
                    auto_now_add=True,
                    verbose_name='created'
                )),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(
                    auto_now=True,
                    verbose_name='modified'
                )),
                ('weight', fields.weight.WeightField(
                    default=100,
                    help_text='weightHelpText',
                    verbose_name='Weight'
                )),
            ],
            options={
                'verbose_name': 'Participant role',
                'verbose_name_plural': 'Participant roles'
            },
        )
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=state_operations,
        )
    ]
