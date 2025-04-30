# https://stackoverflow.com/a/60087190
def _repr(obj):
    return f"{obj.__class__.__name__}({', '.join([f'{k}={v!r}' for k, v in obj.__dict__.items() if not k.startswith('_')])})"
