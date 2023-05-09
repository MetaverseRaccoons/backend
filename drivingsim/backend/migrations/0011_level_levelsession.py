# Generated by Django 4.1.7 on 2023-05-02 13:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0010_user_km_driven_user_minutes_driven_violation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Level',
            fields=[
                ('name', models.TextField(primary_key=True, serialize=False)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='LevelSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('completed', models.BooleanField(default=False)),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.level')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]