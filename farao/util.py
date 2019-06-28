import functools


def partial(func, name: str, *args, **kwargs):
    """
    Like functools.partial, but retains docstring and type-annotations of the
    original function, and gives the partial function the specified name.
    Annotations and a unique name are necessary for auto-creating output paths
    in Task.
    """
    partial_func = functools.partial(func, *args, **kwargs)
    functools.update_wrapper(partial_func, func)
    partial_func.__name__ = name
    return partial_func
