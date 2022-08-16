from django.urls import path
# cache decorator
from django.views.decorators.cache import cache_page

from .views import PostList, PostDetail, PostSearch, PostCreate, PostEdit, PostDelete, MessageList, MessageSearch, \
    MessageCreate, MessageDelete, MessageDetail, msg_accept


app_name = 'board_msg'
urlpatterns = [
    path('', MessageSearch.as_view(), name='msg_list'),
    # with cache
    # path('<int:pk>', cache_page(60*5)(PostDetail.as_view()), name='post_detail'),
    path('<int:pk>', MessageDetail.as_view(), name='msg_detail'),
    # path('search/', MessageSearch.as_view(), name='msg_search'),
    path('create/', MessageCreate.as_view(), name='msg_create'),
    path('<int:pk>/accept/', msg_accept, name='msg_edit'),
    path('<int:pk>/delete/', MessageDelete.as_view(), name='msg_delete'),
]
