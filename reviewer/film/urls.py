from django.urls import path

from film.views import view_index

urlpatterns = [
    path('', view_index, name='index_url'),
]