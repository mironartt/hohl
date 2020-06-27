import random
import string
from django.shortcuts import render, redirect
from django.contrib import admin
from .models.globals import Images, Post, User, Tags, Vacancy
from django.utils.html import format_html
from django.template.defaultfilters import slugify

from core.utils.text import translit

@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):

    # save_on_top = True
    list_display = ['id','title']

@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):

    # save_on_top = True
    list_display = ['image','title', 'description', 'alt',]
    # list_editable = ['moderation']
    # readonly_fields = ['obj_name', ]
    # list_filter = ['moderation', 'watched']
    # search_fields = ('name_person', 'email', 'comment_body',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    save_on_top = True
    list_display = ('id', 'show_image', 'get_slug', 'title', 'short_description', 'get_short_body', 'date_created', 'availavled',)
    readonly_fields = ['show_image', 'date_created', 'get_slug']
    search_fields = ('body', 'title', 'short_description')

    def show_image(self, obj):
        return format_html('<a href="{0}" target="_blank"><img src="{0}" width="150px" /></a>'.format(obj.main_image.image.url))

    def get_short_body(self, obj):
        return obj.body[:800] + '  ......'


    def get_slug(self, obj):
        url = redirect('post', obj.slug).url if obj.slug else '--'
        return format_html('<a href="{0}" target="_blank">{1}</a>'.format(url, '/%s/' % obj.slug if obj.slug else '--'))


    show_image.short_description = 'Главное изображение'
    get_slug.short_description = 'Ссылка на пост'
    get_short_body.short_description = 'Тело поста'
    save_on_top = True

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):

    save_on_top = True
    list_display = ('id', 'show_image', 'get_slug', 'title', 'get_short_body', 'date_created', 'availavled',)
    readonly_fields = ['show_image', 'date_created', 'get_slug']
    search_fields = ('body', 'title', 'short_description')

    def show_image(self, obj):
        return format_html('<a href="{0}" target="_blank"><img src="{0}" width="150px" /></a>'.format(obj.main_image.image.url))

    def get_short_body(self, obj):
        return obj.short_description[:800] + '  ......'


    def get_slug(self, obj):
        url = redirect('post', obj.slug).url if obj.slug else '--'
        return format_html('<a href="{0}" target="_blank">{1}</a>'.format(url, '/%s/' % obj.slug if obj.slug else '--'))


    show_image.short_description = 'Главное изображение'
    get_short_body.short_description = 'Короткое описание'
    save_on_top = True