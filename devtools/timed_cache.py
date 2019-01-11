# Compatibility for version < 1.1
from warnings import warn


def __getattr__(name):
    if name == 'timed_cache':
        warn(f"{name} is deprecated", DeprecationWarning)
        from devtools.cache import timed_cache
        return timed_cache
    else:
        raise AttributeError(f"module {__name__} has no attribute {name}")
