import locale
import os


# from ..exceptions import NotInResourceBundleError, MissingResourceBundleError


class ResourceBundle:
    def __init__(self):
        """Initializes a new ResourceBundle instance

        """
        self._root = "."
        self._parent = None
        self._name = None
        self._lookup = {}
        self._load()

    def get_object(self, key: str) -> object:
        """

        :param key:
        :type key:
        :return:
        :rtype:
        """
        obj = self._handle_get_object(key);
        if obj is None:
            if self._parent is not None:
                obj = self._parent.getObject(key)
            if obj is None:
                # TODO Fix import
                from ..exceptions import NotInResourceBundleError
                raise NotInResourceBundleError("Can't find resource for bundle " + self.get_name() + ", key " + key)
        return obj

    get = get_object

    def _handle_get_object(self, key) -> object:
        """
        Searches the given key in this ResourceBundle and returns its value if found, else None
        :param key:
        :type key:
        :return:
        :rtype:
        """
        try:
            return self._lookup[key]
        except KeyError:
            return None

    def get_name(self) -> str:
        """
        Getter for the name of this ResourceBundle
        :return: The name
        :rtype: str
        """
        return self.name

    def get_bundle(self, basename: str, locale_: locale = None) -> object:
        """
        Gets a bundle
        :param basename: The name of the ResourceBundle
        :type basename: str
        :param locale_: The locale
        :type locale_: locale
        :return: The ResourceBundle
        :rtype: ResourceBundle
        """
        print(basename)
        if locale_ is not None:
            print(locale_)
        else:
            print(locale.getdefaultlocale())
        return None

    def set_parent(self, parent) -> None:
        """Sets the parent for this bundle
        :param parent: The new parent
        :type parent: ResourceBundle
        :return: Nothing
        :rtype: None
        """
        self._parent = parent

    def set_resources_root(self, path: str) -> None:
        """
        Sets the resources root
        :param path: The new path
        :type path: str
        :return: Nothing
        :rtype: None
        """
        if not os.path.exists(path):
            raise FileNotFoundError("'" + path + "' could not be found")
        if os.path.isfile(path):
            raise NotADirectoryError("'" + path + "' is not a directory")
        self._root = path.replace("\\", "/")


if __name__ == '__main__':
    r = ResourceBundle()
    r.get("x")
