
def isnumeric(obj) -> bool:
    """
    Check if an object is a numeric type, i.e. float, int, ndarray etc.
    """

    try:
        obj + 0
        return True

    except TypeError:
        return False

