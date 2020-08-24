# Generated by Django 2.2.15 on 2020-08-24 20:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shows', '0024_show_sponsors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='show',
            name='all_day',
            field=models.BooleanField(default=False, verbose_name='All day'),
        ),
        migrations.AlterField(
            model_name='show',
            name='end',
            field=models.DateTimeField(blank=True, null=True, verbose_name='End'),
        ),
        migrations.AlterField(
            model_name='show',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='locations.Location', verbose_name='Location'),
        ),
        migrations.AlterField(
            model_name='show',
            name='sponsors',
            field=models.ManyToManyField(blank=True, to='profiles.Sponsor'),
        ),
        migrations.AlterField(
            model_name='show',
            name='start',
            field=models.DateTimeField(verbose_name='Start'),
        ),
        migrations.AlterField(
            model_name='showphoto',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='showtypephoto',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]