# Generated by Django 3.1.5 on 2021-02-17 14:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_name', models.TextField(default=0)),
                ('device_mac', models.TextField(default=0)),
                ('sensor_mac', models.TextField(default=0)),
                ('device_model', models.TextField(default=0)),
                ('device_interval', models.TextField(default=0)),
                ('device_version', models.TextField(default=0)),
                ('sensor_model', models.TextField(default=0)),
                ('ch_no', models.TextField(default=0)),
                ('ch_name', models.TextField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='hos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_name', models.TextField(default=0)),
                ('max_temp', models.FloatField(default=0)),
                ('min_temp', models.FloatField(default=0)),
                ('mean_temp', models.FloatField(null=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='We',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('temp', models.FloatField()),
                ('all_temp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='all_temp', to='wan.hos')),
            ],
        ),
    ]
