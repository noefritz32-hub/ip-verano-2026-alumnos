# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def index_page(request):
    return render(request, 'index.html')

def home(request):
    """
    Vista principal que muestra la galería de personajes de Los Simpsons.
    """

    images = services.getAllImages()
    favourite_list = services.getAllFavourites(request)

    return render(
        request,
        'home.html',
        {
            'images': images,
            'favourite_list': favourite_list
        }
    )


def search(request):

    query = request.POST.get("query")

    if not query:
        return redirect('home')

    images = services.filterByCharacter(query)
    favourite_list = []

    return render(
        request,
        'home.html',
        {
            'images': images,
            'favourite_list': favourite_list
        }
    )


def filter_by_status(request):
    """
    Filtra personajes por su estado (Alive/Deceased).
    
    Se debe implementar el filtrado de personajes según su estado.
    Se debe obtener el parámetro 'status' desde el POST, filtrar las imágenes según ese estado
    y renderizar 'home.html' con los resultados. Si no hay estado, redirigir a 'home'.
    """
    pass

# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    """
    Obtiene todos los favoritos del usuario autenticado.
    """
    pass

@login_required
def saveFavourite(request):
    """
    Guarda un personaje como favorito.
    """
    pass

@login_required
def deleteFavourite(request):
    """
    Elimina un favorito del usuario.
    """
    pass

@login_required
def exit(request):
    logout(request)
    return redirect('home')