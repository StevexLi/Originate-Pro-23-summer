# Generated by Django 4.2.4 on 2023-09-05 16:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BasicNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('processed', models.BooleanField(default=False)),
                ('type', models.CharField(default='normal', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='GroupNotification',
            fields=[
                ('basicnotification_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Notification.basicnotification')),
            ],
            bases=('Notification.basicnotification',),
        ),
        migrations.CreateModel(
            name='TeamNotification',
            fields=[
                ('basicnotification_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Notification.basicnotification')),
            ],
            bases=('Notification.basicnotification',),
        ),
    ]
