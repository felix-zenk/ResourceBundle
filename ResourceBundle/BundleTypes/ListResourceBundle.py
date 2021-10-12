import re

from ..util.Locale import Locale
from ..util.readers import ListReader
from .RawResourceBundle import RawResourceBundle, _new_bundle


class ListResourceBundle(RawResourceBundle):

    def __init__(self, path: str = None, root: str = "."):
        """
        Class that handles access to a resource across different locales.
        :param path: The path to the resource file
        :type path: str
        :param root: The resources root directory path
        :type root: str
        """
        super(ListResourceBundle, self).__init__(path, root)
        self._reader = ListReader()
        if path is not None:
            self._name = path
            self._load(path)
        else:
            self._name = "INVALID"

    def _load(self, path: str) -> None:
        """
        Loads keys and values into this BasicResourceBundle instance.
        :param path: The path to the resource file
        :type path: str
        :return: Nothing
        :rtype: None
        """
        if self._root not in path:
            self._reader.load(self._root + "/" + path)
        else:
            self._reader.load(path)
        self._lookup = self._reader.get()

    def _needs_formatting(self, value: list) -> bool:
        for val in value:
            if re.findall(r'{[^}]*}', str(val)):
                return True  # At least one value needs formatting
        return False

    def _format(self, value, *args, **kwargs):
        if self._needs_formatting(value):
            try:
                return self._format(list([
                    (val.format(*args, **kwargs, **self._lookup) if isinstance(val, str) else val)
                    for val in value]))
            except KeyError:
                return self._parent.get(*args, **kwargs, **self._lookup)
        else:
            return value


def get_bundle(base_name: str, locale_: Locale = None, root: str = ".") -> RawResourceBundle:
    """
    Gets a specific ResourceBundle.
    :param base_name: The name of the ResourceBundle
    :type base_name: str
    :param locale_: The locale
    :type locale_: ..util.Locale
    :param root: The resources root directory path
    :type root: str
    :return: The ResourceBundle
    :rtype: BasicResourceBundle
    """
    return _new_bundle(base_name, locale_, "properties", root=root, bundle_type=ListResourceBundle)
