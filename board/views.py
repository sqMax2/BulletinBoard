from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from django.core.cache import cache
from django.forms import CheckboxSelectMultiple
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.utils.translation import gettext as _

import pytz
from django_filters import ModelMultipleChoiceFilter

from .filters import PostFilter, MessageFilter
from .forms import PostForm, ProfileForm, MessageForm
from .models import Post, Message


def set_timezone(request):
    context = {
        'current_time': timezone.localtime(timezone.now()),
        'timezones': pytz.common_timezones
    }
    if request.method == 'POST':
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')
    else:
        return render(request, 'default.html', context)


class PostList(ListView):
    # model name
    model = Post
    # ordering field
    ordering = '-dateCreation'
    # template name
    template_name = 'post_list.html'
    # object list
    context_object_name = 'post_list'
    paginate_by = 10

    # post list generation
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset.filter())
        # current_url = self.request.path
        return self.filterset.qs

    # additional data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # timezone
        # current_time = timezone.now()
        context.update({
            'current_time': timezone.localtime(timezone.now()),
            'timezones': pytz.common_timezones
        })
        # adding filtering object
        context['filterset'] = self.filterset
        return context


class PostSearch(PostList):
    template_name = 'post_search.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # context.update({
    #     #     'current_time': timezone.localtime(timezone.now()),
    #     #     'timezones': pytz.common_timezones
    #     # })
    #     return context


class PostDetail(DetailView):
    # model name
    model = Post
    # template name
    template_name = 'post.html'
    # object name
    context_object_name = 'post'
    queryset = Post.objects.all()

    # cache
    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}',
                        None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'current_time': timezone.localtime(timezone.now()),
            'timezones': pytz.common_timezones
        })
        return context


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # custom form
    form_class = PostForm
    # model
    model = Post
    # template
    template_name = 'post_edit.html'
    permission_required = ('board.add_post',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'current_time': timezone.localtime(timezone.now()),
            'timezones': pytz.common_timezones
        })
        return context

    def form_valid(self, form):
        # current_url = self.request.path
        post = form.save(commit=False)
        self.object = form.save()
        redirectURL = '/posts/' + str(self.object.id)
        return redirect(redirectURL)


class PostEdit(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    # custom form
    form_class = PostForm
    # model
    model = Post
    # template
    template_name = 'post_edit.html'
    permission_required = ('board.change_post',)

    def test_func(self):
        return self.request.user.username == self.get_object().author.username

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'current_time': timezone.localtime(timezone.now()),
            'timezones': pytz.common_timezones
        })
        return context


class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = 'posts/'  # reverse_lazy('post_list')
    permission_required = ('board.delete_post',)

    def test_func(self):
        obj = super().get_object(queryset=self.queryset)
        return self.request.user.username == obj.author.username

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'current_time': timezone.localtime(timezone.now()),
            'timezones': pytz.common_timezones
        })
        return context


class MessageList(ListView):
    # model name
    model = Message
    # ordering field
    ordering = '-dateCreation'
    # template name
    template_name = 'msg_list.html'
    # object list
    context_object_name = 'msg_list'
    paginate_by = 10

    # post list generation
    def get_queryset(self):
        queryset = super().get_queryset().filter(author__email=self.request.user.email) | \
                   super().get_queryset().filter(post__author__email=self.request.user.email)
        self.filterset = MessageFilter(self.request.GET, queryset.filter())
        related_qs = queryset.select_related('post')
        posts_all = Post.objects.all()
        post_qs = Post.objects.none()
        for p in related_qs:
            post_qs |= posts_all.filter(id=p.post.id)
        self.filterset.filters['post_titles'].queryset = post_qs
        # current_url = self.request.path
        return self.filterset.qs

    # additional data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # timezone
        # current_time = timezone.now()
        context.update({
            'current_time': timezone.localtime(timezone.now()),
            'timezones': pytz.common_timezones
        })
        # adding filtering object
        context['filterset'] = self.filterset
        return context


class MessageSearch(MessageList):
    template_name = 'msg_search.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # context.update({
    #     #     'current_time': timezone.localtime(timezone.now()),
    #     #     'timezones': pytz.common_timezones
    #     # })
    #     return context


class MessageCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # custom form
    form_class = MessageForm
    # model
    model = Message
    # template
    template_name = 'msg_edit.html'
    permission_required = ('board.add_message',)

    def __init__(self, *args, **kwargs):
        super(MessageCreate, self).__init__(*args, **kwargs)
        self.post_id = None

    def get(self, request, *args, **kwargs):
        self.post_id = request.GET.get('post')
        return super(MessageCreate, self).get(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     # self.success_url = f'../posts/{self.post_id}'
    #     return super(MessageCreate, self).post(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'current_time': timezone.localtime(timezone.now()),
            'timezones': pytz.common_timezones
        })
        return context

    def form_valid(self, form):
        # current_url = self.request.path
        msg = form.save(commit=False)
        self.post_id = self.request.GET.get("post")
        msg.post = Post.objects.get(id=self.post_id)
        self.object = form.save()
        redirectURL = '/messages/' + str(self.object.id)
        return redirect(redirectURL)


class MessageDetail(DetailView):
    # model name
    model = Message
    # template name
    template_name = 'msg.html'
    # object name
    context_object_name = 'msg'
    queryset = Message.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'current_time': timezone.localtime(timezone.now()),
            'timezones': pytz.common_timezones
        })
        return context


class MessageDelete(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Message
    template_name = 'msg_delete.html'
    success_url = '/messages/'  # reverse_lazy('post_list')
    permission_required = ('board.delete_message',)

    def test_func(self):
        obj = super().get_object(queryset=self.queryset)
        return self.request.user.username == obj.post.author.username

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'current_time': timezone.localtime(timezone.now()),
            'timezones': pytz.common_timezones
        })
        return context


@login_required
def msg_accept(request, **kwargs):
    user = request.user
    msg_id = request.resolver_match.captured_kwargs['pk']
    msg = Message.objects.get(id=msg_id)
    msg_author = msg.author
    post_author = msg.post.author
    if user.email == post_author.email:
        msg.status = True
        msg.save()
    return redirect(msg.get_absolute_url())
