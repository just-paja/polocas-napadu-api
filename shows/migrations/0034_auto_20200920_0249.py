from django.db import migrations

def forward(apps, schema_editor):
    eventModel = apps.get_model('events', 'event')
    showModel = apps.get_model('shows', 'show')
    events = eventModel.objects.all()
    for event in events:
        show = showModel()
        show.__dict__.update(event.__dict__)
        show.show_type2 = event.show_type
        show.save()


def backward(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('shows', '0033_show_show_type2'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
