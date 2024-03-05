# Generated by Django 4.2.4 on 2023-09-05 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('content', models.CharField(max_length=10000)),
                ('is_shared', models.BooleanField(default=False)),
                ('text_url', models.CharField(max_length=100)),
                ('is_write', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='TextHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_id', models.IntegerField()),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('content', models.CharField(max_length=10000)),
            ],
        ),
    ]
