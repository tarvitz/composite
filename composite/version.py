__VERSION__ = (0, 0, 1, 'beta')


def get_version():  #: pragma: no cover
    return ".".join([str(i) for i in __VERSION__[:-1]])


def get_release():  #: pragma: no cover
    return get_version()
