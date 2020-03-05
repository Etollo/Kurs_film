from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [

    path('users/', login_required(UserList.as_view()), name='user_list_url'),
    path('user_json/', user_json, name='user_json_url'),
    path('user/detail/<int:id>', login_required(UserDetail.as_view()), name='user_detail_url'),
    path('user/update/<int:id>', login_required(UserUpdate.as_view()), name='user_update_url'),
    path('user/delete/<int:id>', login_required(UserDelete.as_view()), name='user_delete_url'),
    path('user/create/', login_required(UserCreate.as_view()), name='user_create_url'),
]