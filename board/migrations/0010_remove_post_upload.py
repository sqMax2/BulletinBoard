# Generated by Django 4.1 on 2022-08-12 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0009_alter_post_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='upload',
        ),
    ]
