ALLOWED_HOSTS = ['127.0.0.1']
DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_kurs_film',
        'USER': 'root',
        'PASSWORD': '00000000',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    },
}
