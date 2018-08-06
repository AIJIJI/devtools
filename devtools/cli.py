import os
import sys
from functools import wraps
from termcolor import colored


def error(text):
    print(
        colored(text, 'red', attrs=['bold']),
        file=sys.stdout)


def warn(text):
    print(
        colored(text, 'red'),
        file=sys.stdout)


def environ_required(*environ_args, **environ_kargs):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            environ_kargs.update({i: i for i in environ_args})
            for arg, environ_name in environ_kargs.items():
                try:
                    f.__globals__[arg] = os.environ[environ_name]
                except KeyError as e:
                    error(f'Error: 环境变量 `{environ_name}` 未设置')
                    exit(1)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
