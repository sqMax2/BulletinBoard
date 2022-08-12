from .models import Category, Post, Message
from modeltranslation.translator import register, TranslationOptions

# @register(Category)
# class CategoryTranslationOptions(TranslationOptions):
#     fields = ('name', )


@register(Post)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title', 'text', )


@register(Message)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('text', )


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', )
