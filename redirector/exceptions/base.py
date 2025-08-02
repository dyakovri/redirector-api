class RedirectorException(Exception):
    pass


class NotFoundException(RedirectorException):
    pass


class AlreadyExistsException(RedirectorException):
    pass
