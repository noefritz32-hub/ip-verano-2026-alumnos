# capa de servicio/lógica de negocio

import random
from ..transport import transport
from ..persistence import repositories
from ..utilities import translator


def getAllImages():
    """
    Obtiene todas las imágenes de personajes desde la API y las convierte en objetos Card.
    """

    data = transport.getAllImages()

    cards = []
    for character in data:
        card = translator.fromPostIntoCard(character)
        cards.append(card)

    return cards


def filterByCharacter(name):
    data = transport.getAllImages()

    cards = []

    for character in data:
        card = translator.fromRequestIntoCard(character)

        if name.lower() in card.name.lower():
            cards.append(card)

    return cards


def filter_by_status(status):
    """
    Filtra las cards de personajes según su estado (Alive/Deceased).
    """

    data = transport.getAllImages()
    cards = []

    for character in data:
        card = translator.fromRequestIntoCard(character)

        # protección contra valores vacíos
        if card.status and card.status.lower() == status.lower():
            cards.append(card)

    return cards


# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    """
    Guarda un favorito en la base de datos.
    """

    if not request.user.is_authenticated:
        return

    card = translator.fromPostIntoCard(request.POST)

    # usuario autenticado correcto
    card.user = request.user

    repositories.saveFavourite(card)


def getAllFavourites(request):

    user = request.user

    if not user.is_authenticated:
        return []

    favourites = repositories.getAllFavourites(user) or []

    cards = []

    for fav in favourites:
        card = translator.fromModelIntoCard(fav)
        cards.append(card)

    return cards


def deleteFavourite(request):
    """
    Elimina un favorito de la base de datos.
    """

    fav_id = request.POST.get("id")

    if fav_id:
        repositories.deleteFavourite(fav_id)
