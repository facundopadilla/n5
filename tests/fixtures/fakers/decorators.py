from copy import copy
from functools import wraps


def inject_params(fixture):
    @wraps(fixture)
    def wrapper(request, *args, **kwargs):
        dict_ = copy({})
        if not hasattr(request, "param"):
            request.param = dict_
        return fixture(request=request, *args, **kwargs)

    return wrapper
