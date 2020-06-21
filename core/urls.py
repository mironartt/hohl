
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from .views import index

urlpatterns = [
    path('', index.IndexView.as_view(), name='index'),
    # path('remind-password/<str:remind_password_code>/', index.RemindPasswordInputView.as_view(), name='remind_password_input'),
    # path('remind-password/', index.RemindPasswordView.as_view(), name='remind_password'),
    # path('singin/', index.SingInView.as_view(), name='singin'),
    # path('singup/', index.SingUpView.as_view(), name='singup'),
    # path('lk/', index.UserLkView.as_view(), name='user_lk'),
    # path('blog/<str:post_slug>/', index.PostView.as_view(), name='post'),
    # path('blog/', index.PostListView.as_view(), name='post_list'),
    # path('logout/', index.LogoutView.as_view(), name='logout'),
]