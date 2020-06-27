
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from .views import index

urlpatterns = [
    path('', index.IndexView.as_view(), name='index'),
    path('about-us/', index.AboutUsView.as_view(), name='about_us'),
    path('blog/<str:post_slug>/', index.BlogSingleView.as_view(), name='post'),
    path('contact/', index.ContactView.as_view(), name='contact'),
    path('service/', index.ServiceView.as_view(), name='service'),
    path('why-international-work/', index.WhyIntView.as_view(), name='why_international_work'),
    path('work-list/', index.WorkListView.as_view(), name='work_list'),
    path('blog/', index.BlogView.as_view(), name='blog'),
    # path('logout/', index.LogoutView.as_view(), name='logout'),
]