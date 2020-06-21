from django import template
from core.utils.text import get_translate_base
from django.utils.safestring import SafeString


register = template.Library()

# @register.simple_tag
# def trans_base(text, l_key, cap=False, *args, **kwargs):
#     result = get_translate_base(text, l_key)
#     return result.capitalize() if cap == 1 else (result.upper() if cap == 2 else (result.lower() if cap == 3 else result))
