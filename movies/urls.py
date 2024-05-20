from django.urls import path #Configurar urls para dirigir
from . import views #Importación de las vistas creadas

#urls a direccionar
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:movie_id>/", views.movie_detail, name="movie_detail"),
    path("your_name/", views.get_name, name="get_name"),
    path("<int:movie_id>/review/", views.get_review, name="get_review"),
]