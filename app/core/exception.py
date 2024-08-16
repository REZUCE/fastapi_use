class EventNotFoundException(Exception):
    """
    Raised when event not found.
    """

    def __init__(self, message: str = "Event not found"):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message


class EventsNotFoundTableException(Exception):
    """
    Raised when event not found.
    """

    def __init__(self, message: str = "Event not found in table"):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message


class EventNotUpdateException(Exception):
    """
    Raised when event not found.
    """

    def __init__(self, message: str = "Event could not be update"):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message


class UserAlreadyExistsException(Exception):
    """
    Raised when event not found.
    """

    def __init__(self, message: str = "User already exists with this email"):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message


# Todo: обработать в handlers
class TokenNotCorrectException(Exception):
    """
    Raised when event not found.
    """

    def __init__(self, message: str = "Token is not correct"):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message


class TokenExpireExtension(Exception):
    """
    Raised when event not found.
    """

    def __init__(self, message: str = "Token has expired"):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message

    # detail = "Event not found"

# class EventNotExistsIDException(Exception):
#     """
#     Raised when event with supplied ID does not exist
#     """
#
#     def __init__(self, message: str = "Event with supplied ID does not exist"):
#         self.message = message
#         super().__init__(message)
#
#     def __str__(self):
#         return self.message
#
#     # detail = "Event not found"
