from django.db import models #Importa los modelos de django 
from django.contrib.auth.models import User #Autentificar el usuario en Django
from django.core.validators import MaxValueValidator, MinValueValidator #Validar que los campos estan en el rango predefinido


#Modelo (Tabla) para genero de película y sus atributos
class Genre(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

#Modelo (Tabla) para actores y sus atributos
class Job(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

#Modelo (Tabla) para genero de película y sus atributos
class Person(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

#Modelo (Tabla) para película y sus atributos
class Movie(models.Model):
    title = models.CharField(max_length=200)
    overview = models.TextField()
    release_date = models.DateTimeField()
    running_time = models.IntegerField()
    budget = models.IntegerField(blank=True)
    tmdb_id = models.IntegerField(blank=True, unique=True)
    revenue = models.IntegerField(blank=True)
    poster_path = models.URLField(blank=True)
    genres = models.ManyToManyField(Genre)
    credits = models.ManyToManyField(Person, through="MovieCredit")

    def __str__(self):
        return self.title + ' ' + str(self.release_date.year)

#Modelo (Tabla) para los creditos de la película y sus atributos
class MovieCredit(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)

#Modelo (Tabla) para hcer la reseña de la película y sus atributos
class MovieReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),
                                                          MaxValueValidator(100)])
    review = models.TextField(blank=True)