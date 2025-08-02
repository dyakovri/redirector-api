from .base import NotFoundException


class LinkNotFoundException(NotFoundException):
    pass


class LinkAlreadyExistsException(NotFoundException):
    pass
