from django.http import HttpResponse, HttpResponseRedirect #Devolver un http y redireccionar a otra url
from movies.models import Movie, MovieReview, MovieCredit #Importación de modelos (tablas)
from .forms import NameForm #Importación de formulario para el nombre (Pruebas)
from .formR import ReviewF #Importación de formulario para el review
from django.shortcuts import render, get_object_or_404, redirect #render=devolver html, get_object_or_404=obtener objeto de la BD y lanzar excepción, redirect=dirigir a una url especifica
from django.contrib.auth.models import User #Presenta al usuario
from django.urls import reverse #Obtener url de una vista dando su nombre y parámetros
from django.db.models import Avg #Calucular el promedio

####No se utiliza, se uso como prueba####
def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            print(form.cleaned_data)
            return render(request, "movies/name_ok.html", {"form":form})
    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()
    return render(request, "movies/name.html", {"form": form})

#Función para las reviews
def get_review(request, movie_id):
    #Selectiva para verificar que el usuario inicio sesión sino te direcciona a hacerlo
    if request.user.is_authenticated:
        #Encontrar la película con el ID y si no esta lanzar excepción
        movie = get_object_or_404(Movie, pk=movie_id)
        #Selectiva para verificar que ya se envio el formulario
        if request.method == 'POST':
            #Crear instacia con los datos enviados en la soliciud POST
            form = ReviewF(request.POST)
            #Validar el formulario según las reglas en el formulario
            if form.is_valid():
                #Asiganción de lo valores enviados
                rating = form.cleaned_data['rating']
                review_text = form.cleaned_data['review']
                #Nueva instancia en el modelo, se alamcena en la base de datos del modelo review
                MovieReview.objects.create(user=request.user, movie=movie, rating=rating, review=review_text)
                
                #Redirecciona al html de movie_detail de la película de la cual hiciste la reseña
                return redirect('movie_detail', movie_id=movie_id)
        else:
            #Crear instancia del formulario (GET), inicializando el nombre de a película
            form = ReviewF(initial={'movie_name': movie.title})
        #Retorno del fromulario y plantilla del review para realizar la reseña
        return render(request, 'movies/review.html', {'form': form, 'movie_name': movie.title, 'movie_id': movie_id})
    else:
        #Direcciona a iniciar sesión
        return redirect("http://44.222.13.15:8000/admin/login/")
    #Función para el depliegue del index (índice)
def index(request):
    #Asiganción del modelo
    movies = Movie.objects.all()
    #Asignación de parámetros
    context = {'movie_list': movies}
    #Retorno de variables y solicut de http de la plantilla index.html
    return render(request, "movies/index.html", context=context)

#Función para mostrar los detalles de la película
def movie_detail(request, movie_id):
    #Asiganción de modelos a varaibles en relación al id de la movie
    movie = Movie.objects.get(pk=movie_id)
    reviews = MovieReview.objects.filter(movie=movie)
    actors = MovieCredit.objects.filter(movie=movie)
    
    # Calcular el promedio de los valores de raiting
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    
    #Asignar todo lo que se envia como parámetro
    context = {
        'movie': movie,
        'review_list': reviews,
        'actors': actors,
        'average_rating': average_rating 
    }
    #Retorno a de valores a la plantilla movie_detail.html
    return render(request, "movies/movie_detail.html", context=context)