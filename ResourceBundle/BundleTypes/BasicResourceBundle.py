from ..util.readers import SimpleReader
from ..util.Locale import Locale
from .RawResourceBundle import RawResourceBundle, _new_bundle


class BasicResourceBundle(RawResourceBundle):

    def __init__(self, path: str = None, root: str = "."):
        """
        Class that handles access to a resource across different locales.
        :param path: The path to the resource file
        :type path: str
        :param root: The resources root directory path
        :type root: str
        """
        super(BasicResourceBundle, self).__init__(path, root)
        self._reader = SimpleReader()
        if path is not None:
            self._name = path
            self._load(path)
        else:
            self._name = "INVALID"


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
    return _new_bundle(base_name, locale_, "properties", root=root, bundle_type=BasicResourceBundle)
