# Generated by Django 2.0 on 2018-04-15 21:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSmsProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sms_number', models.CharField(blank=True, default='', max_length=12)),
                ('event_tags', models.CharField(blank=True, default='music', max_length=1000)),
                ('get_notifications', models.BooleanField(default=False, max_length=1000)),
                ('sms_received', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='received_by_user', to='sms.Sms', verbose_name='SMS messages received by user')),
                ('sms_sent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sent_by_user', to='sms.Sms', verbose_name='SMS messages sent by user')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
