# Generated by Django 4.2.4 on 2023-09-05 16:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BasicGroup',
            fields=[
                ('group_id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='GroupChat',
            fields=[
                ('basicgroup_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Chat.basicgroup')),
                ('name', models.CharField(max_length=40)),
                ('type', models.CharField(default='Group', max_length=10)),
                ('has_icon', models.BooleanField(default=False)),
            ],
            bases=('Chat.basicgroup',),
        ),
        migrations.CreateModel(
            name='PrivateChat',
            fields=[
                ('basicgroup_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Chat.basicgroup')),
                ('type', models.CharField(default='Private', max_length=10)),
            ],
            bases=('Chat.basicgroup',),
        ),
        migrations.CreateModel(
            name='TeamGroupChat',
            fields=[
                ('basicgroup_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Chat.basicgroup')),
                ('type', models.CharField(default='Team', max_length=10)),
            ],
            bases=('Chat.basicgroup',),
        ),
        migrations.CreateModel(
            name='MessageEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='message', max_length=20)),
                ('timestamp', models.DateTimeField()),
                ('content', models.TextField()),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group', to='Chat.basicgroup')),
            ],
        ),
    ]