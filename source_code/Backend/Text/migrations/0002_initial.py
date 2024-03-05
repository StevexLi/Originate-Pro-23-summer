# Generated by Django 4.2.4 on 2023-09-05 16:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Text', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Project', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='text',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='text',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Project.project'),
        ),
    ]
