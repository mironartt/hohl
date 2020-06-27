import os
import json
import string
import random
from urllib.parse import urlparse

from datetime import datetime
from django.db.models import Q
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import generic
from django.http import Http404, HttpResponse
from django.utils import timezone
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.contrib import auth, messages
from dateutil.parser import parse

from core.utils.text import check_languages_path, get_confirm_code
from core.utils.mails import send_confirm_code

from core.models import Post, Images, User, Vacancy
from core.forms.site_form import CustomUserCreationForm, CustomAuthenticationForm, RemindPasswordInputForm, \
    RemindPasswordForm


class IndexView(generic.View):
    template_name = 'core/index.html'

    # def dispatch(self, request, *args, **kwargs):
    #     return super(IndexView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, )


class AboutUsView(generic.View):
    template_name = 'core/about__us.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, )

class ContactView(generic.View):

    template_name = 'core/contact.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, )

class WorkListView(generic.View):

    template_name = 'core/work_list.html'
    per_page = 6

    def get(self, request, *args, **kwargs):
        vacansies = Vacancy.objects.filter(
            availavled=True,
        ).order_by('-priority', '-date_created')

        paginator = Paginator(vacansies, self.per_page)
        if paginator.count:
            page = self.request.GET.get('page')
            try:
                vacansies = paginator.page(page)
            except PageNotAnInteger:
                vacansies = paginator.page(1)
            except EmptyPage:
                raise Http404('Error EmptyPage')

        context = {
            'paginator': paginator,
            'vacansies': vacansies,
        }
        return render(request, self.template_name, context)

class WhyIntView(generic.View):

    template_name = 'core/why_internationalwork.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, )


class ServiceView(generic.View):

    template_name = 'core/service.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, )


class BlogSingleView(generic.View):

    template_name = 'core/blog_single.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            self.post = Post.objects.get(slug=kwargs.get('post_slug'))
        except Post.DoesNotExist:
            raise Http404('Post object not find')
        except Post.MultipleObjectsReturned:
            self.post = Post.objects.filter(slug=kwargs.get('post_slug')).first()
            if self.post is None:
                raise Http404('Post object not find after MultipleObjectsReturned')
        return super(BlogSingleView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {
            'post': self.post,
        }
        return render(request, self.template_name, context)


class BlogView(generic.View):

    template_name = 'core/blog.html'
    per_page = 6

    def get(self, request, *args, **kwargs):
        posts = Post.objects.filter(
            availavled=True,
        ).order_by('-priority', '-date_created')

        paginator = Paginator(posts, self.per_page)
        if paginator.count:
            page = self.request.GET.get('page')
            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                posts = paginator.page(1)
            except EmptyPage:
                raise Http404('Error EmptyPage')

        context = {
            'paginator': paginator,
            'posts': posts,
        }
        return render(request, self.template_name, context)