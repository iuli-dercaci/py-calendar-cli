def _get_key_value(key):
    if hasattr(key, 'char'):
        return key.charsdwLU
    elif hasattr(key, 'name'):
        return key.name
    else:
        raise ValueError(f'The key {key} is unknown')


def on_key_press(*args):
    def on_press_decorator(func):
        def on_press_wrapper(key):
            val = _get_key_value(key)
            if val in args:
                return func(key)

        return on_press_wrapper
    return on_press_decorator


def on_key_release(*args):
    def on_release_decorator(func):
        def on_release_wrapper(key):
            val = _get_key_value(key)
            if val in args:
                return func(key)
        return on_release_wrapper
    return on_release_decorator
