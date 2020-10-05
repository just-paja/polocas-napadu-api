# Generated by Django 2.2.16 on 2020-10-04 08:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_auto_20200928_0153'),
        ('theatre_sports', '0025_retarget_event_participant'),
    ]

    state_operations = [
        migrations.CreateModel(
            name='ContestantGroupPlayer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'theatre_sports_contestantgroup_players',
            },
        ),
        migrations.AlterField(
            model_name='contestantgroup',
            name='players',
            field=models.ManyToManyField(related_name='contestant_groups', through='theatre_sports.ContestantGroupPlayer', to='events.EventParticipant', verbose_name='Players'),
        ),
        migrations.AddField(
            model_name='contestantgroupplayer',
            name='contestant_group',
            field=models.ForeignKey(db_column='contestantgroup_id', on_delete=django.db.models.deletion.CASCADE, to='theatre_sports.ContestantGroup'),
        ),
        migrations.AddField(
            model_name='contestantgroupplayer',
            name='participant',
            field=models.ForeignKey(db_column='showparticipant_id', on_delete=django.db.models.deletion.CASCADE, to='events.EventParticipant'),
        ),
    ]
    
    operations = [
        migrations.SeparateDatabaseAndState(state_operations=state_operations)
    ]