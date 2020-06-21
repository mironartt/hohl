import os
import uuid
import random
import string

from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.postgres.fields import JSONField
from django.db.models import Q
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify

from core.utils.text import translit, get_confirm_code

class Images(models.Model):

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    image = models.ImageField(verbose_name='Изображение')
    title = models.CharField(max_length=500, verbose_name='Заголовок', null=True, blank=True)
    description = models.CharField(max_length=500, verbose_name='Описание', null=True, blank=True)
    alt = models.CharField(max_length=80, verbose_name='Краткое описание (alt)', null=True, blank=True)

    def __str__(self):
        return '(id: {0}) {1} {2}'.format(self.id, self.title if self.title else '', '(%s)' % self.alt if self.alt else '')


def user_default_meta_dict():
    return {'confirm_mail_code': get_confirm_code()}

class User(AbstractUser):

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    country = models.CharField(max_length=100, null=True, verbose_name='Страна')
    phone = models.CharField(max_length=20, null=True, verbose_name='Телефон')
    address = models.CharField(max_length=500, null=True, verbose_name='Адрес')
    post_code = models.CharField(max_length=20, null=True, verbose_name='Индекс')
    city = models.CharField(max_length=500, null=True, verbose_name='Город')
    confirm_email = models.BooleanField(default=False, verbose_name='Подтвержден e-mail')
    date_last_emailconfirm_letter = models.DateTimeField(null=True, verbose_name='Дата Последнего отправления подтвержения e-mail')
    meta = JSONField(default=user_default_meta_dict, verbose_name='Дополнительные данные о пользователи')

    def __str__(self):
        return '%s: %s' % (self.id, self.username)


class Post(models.Model):

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты Блога'

    main_image = models.ForeignKey(Images, on_delete=models.CASCADE, verbose_name='Главное изображение поста')
    slug = models.SlugField(verbose_name='Слаг поста (url адрес)', blank=True, null=True)
    title = models.CharField(max_length=500, verbose_name='Заголовок RU', null=True, blank=True)
    short_description = models.CharField(max_length=500, verbose_name='Краткое описание RU', null=True, blank=True)
    body = RichTextUploadingField(verbose_name='Текс на главной странице RU', null=True, blank=True)
    priority = models.IntegerField(default=10, verbose_name='Приоритет в сортировке')
    availavled = models.BooleanField(default=True, verbose_name='Отображать на сайте')

    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    need_sending = models.BooleanField(default=True, verbose_name='Необходимо ли разослать подписчикам уведомление')

    def __str__(self):
        return '({0}) {1}'.format(self.id, self.title)

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)
        slug = self.slug
        if not slug:
            title = '_'.join(self.title.split(' ')[:4]) if self.title else None
            slug = slugify(
                translit(title if title else ''.join(random.choice(string.ascii_lowercase) for _ in range(4))))
        if Post.objects.filter(slug=slug).exclude(id=self.id):
            slug = '%s_%s' % (slug, self.id)
        if self.slug != slug:
            self.slug = slug
            self.save()
