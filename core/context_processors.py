from django.conf import settings
from django.utils.translation import to_locale, get_language

from core.utils.globals import get_css_version


def global_settings(request):
    languages_keys = {
        'ru': 'РУССКИЙ',
        'en': 'ENGLISH',
    }
    language_key = request.session.setdefault('language_key', 'ru')
    return {
        'site_host_name': settings.SITE_DOMAIN,
        'ver_css': get_css_version(),
    }


