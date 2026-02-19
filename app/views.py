# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def index_page(request):
    return render(request, 'index.html')


def home(request):
    """
    Vista principal que muestra la galería de personajes.
    """

    images = services.getAllImages()
    favourite_list = services.getAllFavourites(request)

    return render(request, 'home.html', {
        'images': images,
        'favourite_list': favourite_list
    })


def search(request):
    """
    Busca personajes por nombre.
    """

    if request.method == "POST":

        query = request.POST.get("query")

        if not query or query.strip() == "":
            return redirect('home')

        images = services.filterByCharacter(query)
        favourite_list = services.getAllFavourites(request)

        return render(request, 'home.html', {
            'images': images,
            'favourite_list': favourite_list
        })

    return redirect('home')


def filter_by_status(request):
    """
    Filtra personajes por estado (Alive / Deceased).
    """

    if request.method == "POST":
        status = request.POST.get("status")

        if not status:
            return redirect('home')

        images = services.filter_by_status(status)
        favourite_list = services.getAllFavourites(request)

        return render(request, 'home.html', {
            'images': images,
            'favourite_list': favourite_list
        })

    return redirect('home')


# -------- FAVORITOS --------

@login_required
def getAllFavouritesByUser(request):

    favourite_list = services.getAllFavourites(request)

    return render(request, 'home.html', {
        'images': [],
        'favourite_list': favourite_list
    })


@login_required
def saveFavourite(request):

    if request.method == "POST":
        services.saveFavourite(request)

    return redirect('home')


@login_required
def deleteFavourite(request):

    if request.method == "POST":
        services.deleteFavourite(request)

    return redirect('home')


@login_required
def exit(request):
    logout(request)
    return redirect('home')
