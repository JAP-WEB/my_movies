from django.http import HttpResponse, HttpResponseRedirect #Devolver un http y redireccionar a otra url
from movies.models import Movie, MovieReview, MovieCredit #Importación de modelos (tablas)
from .forms import NameForm #Importación de formulario para el nombre (Pruebas)
from .formR import ReviewF #Importación de formulario para el review
from django.shortcuts import render, get_object_or_404, redirect #render=devolver html, get_object_or_404=obtener objeto de la BD y lanzar excepción, redirect=dirigir a una url especifica
from django.contrib.auth.models import User #Presenta al usuario
from django.urls import reverse #Obtener url de una vista dando su nombre y parámetros
from django.db.models import Avg #Calucular el promedio
from django.contrib.auth import authenticate, login, logout
from .formsU import LoginForm
from django.urls import reverse
from urllib.parse import urlencode
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

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

def user_logout(request):
    logout(request)
    return redirect('index')
    
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
        login_url = reverse('login')
        query_string = urlencode({'next': reverse('movie_detail', args=[movie_id])})
        login_url_with_query = f"{login_url}?{query_string}"
        return redirect(login_url_with_query)

#Función para el depliegue del index (índice)
def index(request):
    # Asiganción del modelo y orden por fecha de lanzamiento en orden descendente
    movies = Movie.objects.all().order_by('-release_date')
    # Asignación de parámetros
    context = {
        'movie_list': movies
    }
    # Retorno de variables y solicitud de HTTP de la plantilla index.html
    return render(request, "movies/index.html", context=context)

#Función para mostrar los detalles de la película
def movie_detail(request, movie_id):
    #Asiganción de modelos a varaibles en relación al id de la movie
    movie = Movie.objects.get(pk=movie_id)
    reviews = MovieReview.objects.filter(movie=movie)
    actors = MovieCredit.objects.filter(movie=movie)
    genres = movie.genres.all()
    
    # Calcular el promedio de los valores de raiting
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    
    recommendations = Movie.objects.filter(genres__in=genres).exclude(id=movie_id).annotate(
        num_genres=Count('genres')
    ).filter(num_genres__gte=2).distinct()
    
    #Asignar todo lo que se envia como parámetro
    context = {
        'movie': movie,
        'review_list': reviews,
        'recommendations': recommendations,
        'actors': actors,
        'average_rating': average_rating 
    }
    #Retorno a de valores a la plantilla movie_detail.html
    return render(request, "movies/movie_detail.html", context=context)
    
def user_login(request):
    next_url = request.GET.get('next', reverse('index'))
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(next_url)
            else:
                # Agregar un mensaje de error
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'movies/login.html', {'form': form, 'login_page': True})
    
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'movies/register.html', {'form': form})

def get_return(request):
    return render(request, 'login.html')
