# Generated by Django 3.0.dev20190119234541 on 2019-01-20 13:51

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('theatre_sports', '0003_auto_20190120_1059'),
    ]

    operations = [
        migrations.CreateModel(
            name='MatchStage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('type', models.PositiveIntegerField(choices=[(2, 'stage-intro'), (3, 'stage-game-setup'), (4, 'stage-game'), (5, 'stage-voting'), (6, 'stage-game-results'), (7, 'stage-pause'), (8, 'stage-finale')])),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stages', to='theatre_sports.Match')),
            ],
            options={
                'verbose_name': 'Match Stage',
                'verbose_name_plural': 'Match Stages',
            },
        ),
    ]
