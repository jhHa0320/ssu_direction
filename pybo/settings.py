import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# TEMPLATES 설정
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
    },
]
