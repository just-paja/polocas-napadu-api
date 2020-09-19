from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shows', '0039_auto_20200920_0346'),
        ('events', '0008_event_participant'),
        ('games', '0010_retarget_event_participant'),
    ]

    state_operations = [
        migrations.DeleteModel('ShowParticipant'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(state_operations=state_operations)
    ]
