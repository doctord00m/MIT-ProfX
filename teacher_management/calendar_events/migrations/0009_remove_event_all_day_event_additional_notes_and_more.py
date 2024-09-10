# Generated by Django 5.1.1 on 2024-09-08 09:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendar_events', '0008_rename_end_time_event_end_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='all_day',
        ),
        migrations.AddField(
            model_name='event',
            name='additional_notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='event_type',
            field=models.CharField(choices=[('Lab Record Submission', 'Lab Record Submission'), ('Viva Voce & Record Submission', 'Viva Voce & Record Submission'), ('Lab midsem exam', 'Lab midsem exam'), ('Midsem Exam', 'Midsem Exam'), ('Quiz', 'Quiz'), ('Assignment', 'Assignment'), ('Test', 'Test')], default='Assignment', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='calendar_events.subject'),
        ),
        migrations.AddField(
            model_name='event',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
