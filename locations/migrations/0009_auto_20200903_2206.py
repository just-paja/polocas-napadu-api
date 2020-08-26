# Generated by Django 2.2.16 on 2020-09-03 20:06

from django.db import migrations
import images.fields


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0008_auto_20200824_2250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locationphoto',
            name='image',
            field=images.fields.ImageField(height_field='height', help_text='imageHelpText', upload_to='var/photos', verbose_name='Image', width_field='width'),
        ),
    ]
