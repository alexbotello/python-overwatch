class InvalidFilter(Exception):
    """
    Raise when 'filter' key word argument is not recognized
    """
    pass


class InvalidHero(Exception):
    """
    Raise when 'hero' key word argument is not recognized
    """
    pass


class InvalidCombination(Exception):
    """
    Raise when 'filter' and 'hero' key word arguments
    are an invalid combination.
    """
    pass


class NotFound(Exception):
    """
    Raise when stats could not be found
    """
    pass
