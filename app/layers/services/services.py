# capa de servicio/lógica de negocio

import random
from ..transport import transport
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user

def getAllImages():
    """
    Obtiene todas las imágenes de personajes desde la API y las convierte en objetos Card.
    
    Esta función debe obtener los datos desde transport, transformarlos en Cards usando 
    translator y retornar una lista de objetos Card.
    """

    data = transport.getAllImages()

    cards = []
    for character in data:
        card = translator.fromRequestIntoCard(character)
        cards.append(card)

    return cards
def filter_images_by_status(status):

    cards = getAllImages()
    filtered = []

    for card in cards:
        if card.status == status:
            filtered.append(card)

    return filtered

def filterByCharacter(name):
    data = transport.getAllImages()

    cards = []

    for character in data:
        card = translator.fromRequestIntoCard(character)

        if name.lower() in card.name.lower():
            cards.append(card)

    return cards


def filterByStatus(status_name):
    """
    Filtra las cards de personajes según su estado (Alive/Deceased).
    
    Se deben filtrar los personajes que tengan el estado igual al parámetro 'status_name'. Retorna una lista de Cards filtradas.
    """

    data = transport.getAllImages()
    cards = []

    for character in data:
        card = translator.fromRequestIntoCard(character)

        # protección contra valores vacíos
        if card.status and card.status.lower() == status_name.lower():
            cards.append(card)

    return cards


# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    """
    Guarda un favorito en la base de datos.
    
    Se deben convertir los datos del request en una Card usando el translator,
    asignarle el usuario actual, y guardarla en el repositorio.
    """
    user = get_user(request)

    if not user.is_authenticated:
        return

    # convierte datos del POST en Card
    card = translator.fromRequestIntoCard(request.POST)

    # asigna usuario
    card.user = user

    repositories.saveFavourite(card)


def getAllFavourites(request):
    """
    Obtiene todos los favoritos del usuario autenticado.
    
    Si el usuario está autenticado, se deben obtener sus favoritos desde el repositorio,
    transformarlos en Cards usando translator y retornar la lista. Si no está autenticado, se retorna una lista vacía.
    """
    user = get_user(request)

    if not user.is_authenticated:
        return []

    favourites = repositories.getAllFavouritesByUser(user)

    cards = []

    for fav in favourites:
        card = translator.fromModelIntoCard(fav)
        cards.append(card)

    return cards



def deleteFavourite(request):
    """
    Elimina un favorito de la base de datos.
    
    Se debe obtener el ID del favorito desde el POST y eliminarlo desde el repositorio.
    """
    fav_id = request.POST.get("id")

    if fav_id:
        repositories.deleteFavourite(fav_id)