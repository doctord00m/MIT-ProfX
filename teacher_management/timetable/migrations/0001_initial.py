# Generated by Django 5.0.2 on 2024-08-20 05:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
from django.utils import timezone


def create_default_subject(apps, schema_editor):
    Subject = apps.get_model('timetable', 'Subject')
    Subject.objects.create(name='Default Subject')


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('day', models.CharField(choices=[('MON', 'Monday'), ('TUE', 'Tuesday'), ('WED', 'Wednesday'), ('THU', 'Thursday'), ('FRI', 'Friday'), ('SAT', 'Saturday'), ('SUN', 'Sunday')], max_length=10)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('room', models.CharField(max_length=50)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TimetableChangeRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proposed_day', models.CharField(choices=[('MON', 'Monday'), ('TUE', 'Tuesday'), ('WED', 'Wednesday'), ('THU', 'Thursday'), ('FRI', 'Friday'), ('SAT', 'Saturday'), ('SUN', 'Sunday')], max_length=10)),
                ('proposed_start_time', models.TimeField()),
                ('proposed_end_time', models.TimeField()),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('DENIED', 'Denied')], default='PENDING', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('original_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='change_requests', to='timetable.class')),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='change_requests', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RunPython(create_default_subject),
    ]
