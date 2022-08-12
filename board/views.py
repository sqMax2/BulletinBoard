from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.cache import cache
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

import pytz

from .filters import PostFilter
from .forms import PostForm, ProfileForm
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


class PostCreate(PermissionRequiredMixin, CreateView):
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


class PostEdit(PermissionRequiredMixin, UpdateView):
    # custom form
    form_class = PostForm
    # model
    model = Post
    # template
    template_name = 'post_edit.html'
    permission_required = ('board.change_post',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'current_time': timezone.localtime(timezone.now()),
            'timezones': pytz.common_timezones
        })
        return context


class PostDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
    permission_required = ('board.delete_post',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'current_time': timezone.localtime(timezone.now()),
            'timezones': pytz.common_timezones
        })
        return context
