from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User

from modeltranslation.admin import TranslationAdmin

from .models import Category, Post, Message


class CategoryAdmin(ModelAdmin):
    list_display = ['name', 'post_count', ]


class PostAdmin(TranslationAdmin):
    # list_display = ['title', ]
    # filter_horizontal = ['postCategory', ]
    # fields = ('title', 'author', 'text', 'categoryType', )
    list_display = ['id', 'title', 'dateCreation', 'author', 'author_email', 'no_category',
                    'postCategory', ]
    list_display_links = ['title']
    list_filter = ['postCategory']
    search_fields = ['author__authorUser__username']

    @admin.display(description="Author's email")
    def author_email(self, obj):
        return obj.author.email


class MessageAdmin(TranslationAdmin):
    list_display = ['__str__', 'author', 'status', 'post', ]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Message, MessageAdmin)
