from django.db.models import Prefetch
from django_filters import FilterSet, ModelMultipleChoiceFilter, DateFilter, ChoiceFilter
from django.forms import DateInput, CheckboxSelectMultiple, RadioSelect
from django.utils.translation import gettext as _

from .models import Category, Post, Message


class PostFilter(FilterSet):
    # category field filter
    # category = ModelMultipleChoiceFilter(
    #     field_name='postcategory__categoryThrough',
    #     queryset=Category.objects.all(),
    #     label=_('Category'),
    #     widget=CheckboxSelectMultiple(),
    #     # empty_label='any'
    # )
    # changing default date selector to calendar view

    date_widget = DateInput()
    date_widget.input_type = 'date'
    dateCreation = DateFilter(
        field_name='dateCreation',
        lookup_expr='gte',
        widget=date_widget,
        label=_('Creation date since')
    )

    class Meta:
        # model
        model = Post
        # filtering fields
        fields = {
            # news title
            'title': ['icontains'],
        }

    def __init__(self, *args, **kwargs):
        super(PostFilter, self).__init__(*args, **kwargs)
        self.filters['title__icontains'].label = _('Title contains:')


class MessageFilter(FilterSet):
    # Post titles filter
    post_titles = ModelMultipleChoiceFilter(
        field_name='post',
        queryset=Post.objects.none(),
        label=_('Filter by posts'),
        widget=CheckboxSelectMultiple(),
    )
    date_widget = DateInput()
    date_widget.input_type = 'date'
    dateCreation = DateFilter(
        field_name='dateCreation',
        lookup_expr='gte',
        widget=date_widget,
        label=_('Creation date since')
    )

    class Meta:
        # model
        model = Message
        # filtering fields
        fields = {
            'text': ['icontains'],
        }

    def __init__(self, *args, **kwargs):
        super(MessageFilter, self).__init__(*args, **kwargs)
        self.filters['text__icontains'].label = _('Text contains:')
