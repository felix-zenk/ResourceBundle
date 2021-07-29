from ..util.Locale import Locale
from .RawResourceBundle import RawResourceBundle, _new_bundle
from util.readers import ListReader


class ListResourceBundle(RawResourceBundle):
    def __init__(self, path: str = None, root: str = "."):
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
