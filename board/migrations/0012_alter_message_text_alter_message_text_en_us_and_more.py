# Generated by Django 4.1 on 2022-08-15 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0011_alter_message_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='text',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='message',
            name='text_en_us',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='text_ru',
            field=models.TextField(null=True),
        ),
    ]
