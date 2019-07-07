import functools
import re


def partial(func, name: str, *args, **kwargs):
    """
    Like functools.partial, but retains docstring and type-annotations of the
    original function, and gives the partial function the specified name.
    Annotations and a unique name are necessary for auto-creating output paths
    of tasks.
    """
    partial_func = functools.partial(func, *args, **kwargs)
    functools.update_wrapper(partial_func, func)
    partial_func.__name__ = name
    return partial_func


def linearize(multiline: str) -> str:
    """
    :param multiline:  A multiline string as found in indented source code.
    :return:  A stripped, one-line string. All newlines and multiple
            consecutive whitespace characters are replaced by a single space.
    """
    oneline = re.sub(r"\s+", " ", multiline)
    return oneline.strip()
