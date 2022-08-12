from django.urls import path
# cache decorator
from django.views.decorators.cache import cache_page

from .views import PostList, PostDetail, PostSearch, PostCreate, PostEdit, PostDelete



app_name = 'newsapp'
urlpatterns = [
    path('', cache_page(30)(PostList.as_view()), name='post_list'),
    # with cache
    # path('<int:pk>', cache_page(60*5)(PostDetail.as_view()), name='post_detail'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
]
