from string import Template

from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.utils.translation import gettext as _
from ckeditor.fields import RichTextField


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
    text = RichTextField()
    postCategory = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts', verbose_name='Category')
    rating = models.SmallIntegerField(default=0)

    template_string = '$text...'

    # Rating modifiers
    def like(self):
        self.rating += 1
        self.save()

    @property
    def no_category(self):
        return not self.postCategory.all().exists()

    def preview(self):
        return Template(self.template_string).substitute(text=self.text[0:123])

    def __str__(self):
        return f'{self.title} {self.dateCreation}: {Template(self.template_string).substitute(text=self.text[0:20])}...'

    # deletes cache on post save
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # removes cache
        cache.delete(f'post-{self.pk}')


class Message(models.Model):
    messagePost = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='messages', verbose_name='Message')
    messageUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages', verbose_name='User')
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True, verbose_name='Creation date')

    template_string = '$text...'

    def __str__(self):
        return f'{self.messagePost.title}: {self.messageUser.username}: ' \
               f'{Template(self.template_string).substitute(text=self.text[0:20])}... {self.dateCreation}'
