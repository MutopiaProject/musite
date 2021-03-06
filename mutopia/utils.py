"""
.. module:: utils
   :platform: Linux
   :synopsis: Miscellaneous utility functions

.. moduleauthor:: Glen Larsen <glenl.glx@gmail.com>

"""

import os
import re
import datetime

MUTOPIA_BASE = 'MUTOPIA_BASE'
MUTOPIA_WEB = 'MUTOPIA_WEB'
MUTOPIA_URL = 'http://www.mutopiaproject.org'
FTP_URL = MUTOPIA_URL + '/ftp'
GITHUB_REPOS = 'https://api.github.com/repos/MutopiaProject/MutopiaProject'

__all__ = [
    'MUTOPIA_BASE',
    'MUTOPIA_WEB',
    'MUTOPIA_URL',
    'FTP_URL',
    'GITHUB_REPOS',
]


class Singleton:
    """
    A non-thread-safe helper class to ease implementing singletons.
    This should be used as a decorator -- not a metaclass -- to the
    class that should be a singleton.

    The decorated class can define one `__init__` function that
    takes only the `self` argument. Other than that, there are
    no restrictions that apply to the decorated class.

    To get the singleton instance, use the `Instance` method. Trying
    to use `__call__` will result in a `TypeError` being raised.

    Limitations: The decorated class cannot be inherited from.
    """

    def __init__(self, decorated):
        self._decorated = decorated

    def Instance(self):
        """Returns the singleton instance.

        Returns:
            Upon its first call, it creates a new instance of the
            decorated class and calls its `__init__` method. On all
            subsequent calls, the already created instance is returned.
        """
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)


_MUID_PATTERN = re.compile('Mutopia-([0-9]{4})/(\d\d?)/(\d\d?)-([0-9]*)$')
def parse_mutopia_id(mutopia_id):
    """Parse a Mutopia mutopia_id string, typically from an RDF file, and
    return a tuple containing the publication date and piece-id.

    For example::

        Mutopia-2016/20/12-33 ==> ("2016/20/12", "33")
        Mutopia-2016/20/12-AB ==> None

    :param str mutopia_id: The mutopia mutopia_id string, expected to be in
        the appropriate format.
    :return: A tuple containing a (datetime.date, id)

    """
    if mutopia_id:
        fmat = _MUID_PATTERN.search(mutopia_id)
        if fmat:
            try:
                pub_date = datetime.date(int(fmat.group(1)),
                                         int(fmat.group(2)),
                                         int(fmat.group(3)))
                return (pub_date, fmat.group(4))
            except TypeError:
                raise ValueError('Invalid date on input from %s' % fmat.group(0))

    raise ValueError('Empty or mal-formed mutopia id')
