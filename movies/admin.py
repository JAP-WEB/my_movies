from django.contrib import admin #admin la parte de gestión administrativa de Django

from movies.models import Movie, Genre, Job, Person, MovieCredit, MovieReview 

#Gestión de modelos (crear, leer, actualizar, y eliminar registros) a través de la interfaz administrativa proporcionada por Django
admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(Job)
admin.site.register(Person)
admin.site.register(MovieCredit)
admin.site.register(MovieReview)