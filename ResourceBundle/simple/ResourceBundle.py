import os

from typing import List, KeysView

from ..util.Locale import Locale
from ..util.readers import SimpleReader
from ..exceptions import NotInResourceBundleError, MissingResourceBundleError


class ResourceBundle:
    """
    Class that handles access to a resource across different locales
    """

    cached_bundles = {}

    def __init__(self, path: str = None, root: str = None):
        """
        Initializes a new ResourceBundle instance and loads the given resource file
        :param path: The path to the resource file
        :type path: str
        :param root: The resources root directory path
        :type root: str
        """
        self._parent = None
        self._name = path
        self._lookup = {}
        self._reader = SimpleReader()
        if root is None:
            self._root = "."
        else:
            self.set_resources_root(root)
        if path is not None:
            self._load(path)

    def _load(self, path: str) -> None:
        """
        Loads keys and values into this ResourceBundle instance
        :param path: The path to the resource file
        :type path: str
        :return: Nothing
        :rtype: None
        """
        self._reader.load(self._root + "/" + path)
        self._lookup = self._reader.get()

    def get(self, key: str) -> str:
        """
        Gets an object from the ResourceBundle
        :param key: The key of the desired object
        :type key: str
        :return: The object
        :rtype: str
        """
        obj = self._handle_get_object(key)
        if obj is None:
            if self._parent is not None:
                obj = self._parent.get(key)
            if obj is None:
                raise NotInResourceBundleError("Can't find resource for bundle " + self.get_name() + ", key " + key)
        return obj

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

    def set_name(self, name):
        """
        Setter for the name of this ResourceBundle
        :param name: The new name
        :type name: str
        :return: Nothing
        :rtype: None
        """
        self._name = name

    def get_name(self) -> str:
        """
        Getter for the name of this ResourceBundle
        :return: The name
        :rtype: str
        """
        return self._name

    def get_keys(self) -> KeysView:
        """
        Gets the currently loaded keys
        :return: The keys
        :rtype: List[str]
        """
        return self._lookup.keys()

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
        path = path.replace("\\", "/")
        if path.endswith("/"):
            path = path[:-1]
        if not os.path.exists(path):
            raise FileNotFoundError("'" + path + "' could not be found")
        if os.path.isfile(path):
            raise NotADirectoryError("'" + path + "' is not a directory")
        self._root = path
        if self._parent is not None:
            self._parent.set_resources_root(path)

    def generate_parent_chain(self, base_name: str, locale_: Locale, root: str = None) -> None:
        """
        Generates the parent chain for this ResourceBundle
        :param base_name:
        :type base_name:
        :param locale_:
        :type locale_:
        :param root: The resources root directory path
        :type root: str
        :return: Nothing
        :rtype: None
        """
        top_locale = locale_.get_top_locale()
        self.cached_bundles[_to_bundle_name(base_name, locale_)] = self
        if top_locale is None:
            return
        else:
            try:
                bundle = self.cached_bundles[_to_bundle_name(base_name, top_locale)]
            except KeyError:
                bundle = get_bundle(base_name, top_locale, root=root)  # TODO Try set parent bundle / maybe skip -> parent.parent /maybe is most top bundle -> None
            self.set_parent(bundle)


def get_bundle(base_name: str, locale_: Locale = None, root: str = None) -> ResourceBundle:
    """
    Gets a specific ResourceBundle
    :param base_name: The name of the ResourceBundle
    :type base_name: str
    :param locale_: The locale
    :type locale_: ..util.Locale
    :param root: The resources root directory path
    :type root: str
    :return: The ResourceBundle
    :rtype: ResourceBundle
    """
    return _new_bundle(base_name, locale_, "properties", root)


def _to_resource_name(bundle_name: str, format_: str) -> str:
    """
    Converts the ResourceBundle name into the corresponding resource path
    :param bundle_name: The specific name of the ResourceBundle
    :type bundle_name: str
    :param format_: The format of this ResourceBundle (file extension)
    :type format_: str
    :return: The resource name
    :rtype: str
    """
    return bundle_name + "." + format_


def _to_bundle_name(base_name: str, locale_: Locale) -> str:
    """
    Generates the bundle name for a ResourceBundle
    :param base_name: The base name of the ResourceBundle
    :type base_name: str
    :param locale_: The locale to use for generating the name
    :type locale_: ..util.Locale
    :return: The name of the ResourceBundle
    :rtype: str
    """
    return base_name + locale_.get_delim() + locale_.to_string() if locale_.to_string() != "" else base_name


def _new_bundle(base_name: str, locale_: Locale, format_: str, root: str = None) -> ResourceBundle:
    """
    Creates a new ResourceBundle
    :param base_name: The base name of this ResourceBundle
    :type base_name: str
    :param locale_: The locale for this ResourceBundle
    :type locale_: ..util.Locale
    :param format_: The format (file extension)
    :type format_: str
    :param root: The resources root directory path
    :type root: str
    :return: The new ResourceBundle
    :rtype: ResourceBundle
    """
    bundle = ResourceBundle(_to_resource_name(_to_bundle_name(base_name, locale_), format_), root)
    bundle.generate_parent_chain(base_name, locale_, root)
    return bundle