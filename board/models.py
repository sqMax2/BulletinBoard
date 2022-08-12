from string import Template
import re

from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.html import strip_tags
from django.utils.translation import gettext as _

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True, help_text=_('category name'))

    @property
    def post_count(self):
        return self.posts.count()

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Author')
    dateCreation = models.DateTimeField(auto_now_add=True, verbose_name='Creation date')
    title = models.CharField(max_length=128, verbose_name=_('Title'))
    text = RichTextUploadingField()
    postCategory = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts', verbose_name='Category')
    rating = models.SmallIntegerField(default=0)
    # upload = models.FileField(upload_to='upload/', default=None)

    template_string = '$text...'

    # Rating modifiers
    def like(self):
        self.rating += 1
        self.save()

    @property
    def no_category(self):
        return not self.postCategory

    def textify(self, html):
        # Remove html tags and continuous whitespaces
        templatedHTML = Template(self.template_string).substitute(text=html)
        print(templatedHTML)
        text_only = re.sub('[ \t]+', ' ', strip_tags(templatedHTML))
        text_only = re.sub('&nbsp;', ' ', text_only)
        # Strip single spaces in the beginning of each line
        return text_only.replace('\n ', '\n').strip()
        # return strip_tags(Template(self.template_string).substitute(text=self.text))

    @property
    def plainText(self):
        return self.textify(self.text)

    def preview(self):
        return self.textify(self.text)[0:123]  # Template(self.template_string).substitute(text=self.text[0:123])

    def __str__(self):
        return f'{self.title} {self.dateCreation}: {self.textify(self.text)[0:20]}...'

    # deletes cache on post save
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # removes cache
        cache.delete(f'post-{self.pk}')

    # returns post URL
    def get_absolute_url(self):
        return reverse_lazy('board:post_detail', args=['posts', str(self.id)])


class Message(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='messages', verbose_name='Post')
    author = models.OneToOneField(User, on_delete=models.CASCADE, related_name='messages', verbose_name='User')
    text = RichTextField()
    dateCreation = models.DateTimeField(auto_now_add=True, verbose_name='Creation date')
    status = models.BooleanField(default=False)

    template_string = '$text...'

    def __str__(self):
        return f'{self.messagePost.title}: {self.messageUser.username}: ' \
               f'{Template(self.template_string).substitute(text=self.text[0:20])}... {self.dateCreation}'


class NewUser(User):
    status = models.BooleanField(default=False)
    auth_code = models.CharField(max_length=128)
