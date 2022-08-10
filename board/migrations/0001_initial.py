# Generated by Django 4.1 on 2022-08-10 16:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='category name', max_length=64, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateCreation', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('title', models.CharField(max_length=128, verbose_name='Title')),
                ('text', models.TextField()),
                ('rating', models.SmallIntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('postCategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='board.category', verbose_name='Category')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('dateCreation', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('messagePost', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='board.post', verbose_name='Message')),
                ('messageUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
    ]
