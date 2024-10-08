# Generated by Django 5.1 on 2024-08-30 04:54

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("calendar_events", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Subject",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name="event",
            name="attendees",
        ),
        migrations.RemoveField(
            model_name="event",
            name="google_calendar_event_id",
        ),
        migrations.AddField(
            model_name="event",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="event",
            name="event_type",
            field=models.CharField(
                choices=[
                    ("ASSIGNMENT", "Assignment"),
                    ("EXAM", "Exam"),
                    ("SUBMISSION", "Submission"),
                    ("VIVA", "Viva-Voce"),
                ],
                default='ASSIGNMENT',
                max_length=20,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='event_type',
            field=models.CharField(choices=[('ASSIGNMENT', 'Assignment'), ('EXAM', 'Exam'), ('SUBMISSION', 'Submission'), ('VIVA', 'Viva-Voce')], default='ASSIGNMENT', max_length=20),
        ),
        migrations.AlterField(
            model_name="event",
            name="created_by",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="description",
            field=models.TextField(),
        ),
        migrations.AddField(
            model_name="event",
            name="subject",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="calendar_events.subject",
            ),
            preserve_default=False,
        ),
    ]

def create_default_subject(apps, schema_editor):
    Subject = apps.get_model('calendar_events', 'Subject')
    Subject.objects.create(name='Default Subject')
