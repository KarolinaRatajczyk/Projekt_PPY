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



