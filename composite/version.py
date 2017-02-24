__VERSION__ = (0, 1, 0, 'release')


def get_version():  #: pragma: no cover
    return ".".join(str(i) for i in __VERSION__[:-1])


def get_release():  #: pragma: no cover
    return get_version()
