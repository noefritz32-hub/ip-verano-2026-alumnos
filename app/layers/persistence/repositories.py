# capa DAO de acceso/persistencia de datos.

from app.models import Favourite


def saveFavourite(fav):
    """
    Guarda un favorito en la base de datos.
    """
    favourite = Favourite.objects.create(
        name=fav.name,
        gender=fav.gender,
        status=fav.status,
        occupation=fav.occupation,
        phrases=fav.phrases,
        age=fav.age,
        image=fav.image,
        user=fav.user
    )
    return favourite


def getAllFavourites(user):
    """
    Obtiene todos los favoritos de un usuario.
    """
    return Favourite.objects.filter(user=user)


def deleteFavourite(favId):
    """
    Elimina un favorito por ID.
    """
    favourite = Favourite.objects.get(id=favId)
    favourite.delete()
    return True
