# Generated by Django 4.2.4 on 2023-09-05 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('introduction', models.CharField(max_length=60)),
                ('has_icon', models.BooleanField(default=False)),
            ],
        ),
    ]
