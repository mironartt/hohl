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

from core.models import Post, Images, User
from core.forms.site_form import CustomUserCreationForm, CustomAuthenticationForm, RemindPasswordInputForm, RemindPasswordForm


class IndexView(generic.View):
    template_name = 'core/index.html'

    # def dispatch(self, request, *args, **kwargs):
    #     return super(IndexView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name,)


