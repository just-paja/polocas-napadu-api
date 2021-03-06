# Generated by Django 2.2.1 on 2019-05-23 05:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("voting", "0005_livepollvoting_avg_volume"),
        ("shows", "0008_showvolumecalibration"),
    ]

    operations = [
        migrations.CreateModel(
            name="ShowVolumeCalibrationVoting",
            fields=[
                (
                    "livepollvoting_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="voting.LivePollVoting",
                    ),
                ),
                (
                    "calibration",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="calibration_votings",
                        to="shows.ShowVolumeCalibration",
                    ),
                ),
            ],
            options={
                "verbose_name": "Show volume calibration voting",
                "verbose_name_plural": "Show volume calibrations voting",
            },
            bases=("voting.livepollvoting",),
        ),
    ]
