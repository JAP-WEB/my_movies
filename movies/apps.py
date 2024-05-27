#permite que Django pueda identificar y manejar correctamente la aplicación dentro del proyecto
from django.apps import AppConfig


class MoviesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movies'
