class WrongStatus(Exception):
    "When wrong status"
    pass

class NotSuchAnId(Exception):
    "When there is no such an id"
    pass

class DuplicateMovieError(Exception):
    "when there is a duplicate"
    pass

class EmptyMovieListError(Exception):
    "no deleting - it's empty"
    pass

class WrongFileLoading(Exception):
    "when wrong file loading"
    pass

class UserError(Exception):
    "when user error"
    pass

class UserAlreadyExists(Exception):
    "User already exists"
    pass

class IncorrectPassword(Exception):
    "Incorrect password"
    pass

class InvalidRatingError(Exception):
    "Rating must be a number between 0 and 10"
    pass

class MovieNotSelectedError(Exception):
    "No movie selected"
    pass
