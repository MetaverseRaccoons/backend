# Generated by Django 4.1.3 on 2022-12-05 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_student',
            new_name='is_learner',
        ),
    ]
