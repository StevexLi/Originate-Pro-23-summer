# Generated by Django 4.2.4 on 2023-09-05 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Graph',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('content', models.CharField(max_length=10000)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('introduction', models.CharField(max_length=60)),
                ('width', models.IntegerField(blank=True, default=800, null=True)),
                ('has_document', models.BooleanField(default=False)),
                ('is_shared', models.BooleanField(default=False)),
            ],
        ),
    ]
