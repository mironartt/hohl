import random
import string
from django.conf import settings

def translit(text):
    _from = [
        'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф',
        'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я', ' ', '№', '`', '»', '«', '/', '\\', ':', '“', '”', '"',
        '#', '%', '?'
    ]
    _to = [
        'a', 'b', 'v', 'g', 'd', 'e', 'yo', 'zh', 'z', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'f',
        'h', 'c', 'ch', 'sh', 'sсh', '', 'y', '', 'je', 'ju', 'ja', '_', 'No', '-', '', '', '-', '-', '', '', '', '',
        'No', '_', ''
    ]
    text = text.lower()
    for i, value in enumerate(_from):
        text = text.replace(_from[i], _to[i])
    return text

def check_languages_path(path):
    for lang_key in settings.PROJECT_LANGUAGES:
        # print(' path.count >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> key: {0}  || count: {1}  || result: {2}'.format(lang_key, path.count('/%s/' % lang_key), ''))
        if path.count('/%s/' % lang_key) > 1:
            return False
    return True


def get_translate_base(text='Имя', key='en'):
    text = text.strip().lower()
    with open('translates/globals.txt', 'rt') as file_dict:
        for row in file_dict:
            row = row.strip().lower()
            if ':%  s|' % text in row:
                for i in row.split('|')[:-1]:
                    if i[:3] == '%s:' % key:
                        return i.replace('%s:' % key, '')
    # if settings.DEBUG:
    #     raise ('not find translate')
    return text

def get_confirm_code(count_simvol=20):
    return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(count_simvol))


