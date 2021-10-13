import re
from typing import List, Type
from os.path import exists, isfile, join

from ..util.Locale import Locale, ROOT_LOCALE, from_iso
from ..exceptions import NotInResourceBundleError, MissingResourceBundleError


_STANDARD_FILE_EXTENSION = "properties"


class RawResourceBundle:
    _cached_bundles = {}

    def __init__(self, path: str = None, root: str = "."):
        """
        Class that handles access to a resource across different locales.
        :param path: The path to the resource file
        :type path: str
        :param root: The resources root directory path
        :type root: str
        """
        self._root = "."  # Initialize root
        self._parent = None
        self._lookup = {}
        self._reader = None
        self.set_resources_root(root)  # Set correct root
        self._name = "INVALID" if path is None else path


    def _load(self, path: str) -> None:
        """
        Loads keys and values into this BasicResourceBundle instance.
        :param path: The path to the resource file
        :type path: str
        :return: Nothing
        :rtype: None
        """
        if self._root not in path:
            self._reader.load(join(self._root, path))
        else:
            self._reader.load(path)
        self._lookup = self._reader.get()

    def _needs_formatting(self, value: str) -> bool:
        return re.findall(r'{[^}]*}', value)

    def _format(self, value, *args, **kwargs):
        if self._needs_formatting(value):
            try:
                return self._format(value.format(*args, **kwargs, **self._lookup))
            except KeyError:
                return self._parent._format(value, *args, **kwargs)
        else:
            return value

    def _handle_get_object(self, key, *args, **kwargs) -> object:
        """
        Searches the given key in this ResourceBundle and returns its value if found, else None.
        :param key:
        :type key:
        :return:
        :rtype:
        """
        try:
            return self._format(self._lookup[key], *args, **kwargs) \
                if self._needs_formatting(self._lookup[key]) \
                else self._lookup[key]
        except KeyError:
            return None

    def _set_parent(self, parent) -> None:
        """
        Sets the parent for this bundle.
        :param parent: The new parent
        :type parent: BasicResourceBundle
        :return: Nothing
        :rtype: None
        """
        self._parent = parent

    def set_resources_root(self, path: str) -> None:
        """
        Sets the resources root.
        :param path: The new path
        :type path: str
        :return: Nothing
        :rtype: None
        """
        path = path.replace("\\", "/")
        if path.endswith("/"):
            path = path[:-1]
        if not exists(path):
            raise FileNotFoundError("'" + path + "' could not be found")
        if isfile(path):
            raise NotADirectoryError("'" + path + "' is not a directory")
        self._root = path
        if self._parent is not None:
            self._parent.set_resources_root(path)

    def generate_parent_chain(self, base_name: str, locale_: Locale, root: str = None) -> None:
        """
        Generates the parent chain for this BasicResourceBundle.
        :param bundle_type: The type of bundle to create
        :type bundle_type: RawResourceBundle
        :param base_name: The base name of this bundle
        :type base_name: str
        :param locale_: The Locale of this ResourceBundle
        :type locale_: Locale
        :param root: The resources root directory path
        :type root: str
        :return: Nothing
        :rtype: None
        """
        top_locale = locale_.get_top_locale()
        self._cached_bundles[_to_bundle_name(base_name, locale_)] = self
        if top_locale is None:
            return
        else:
            try:
                bundle = self._cached_bundles[_to_bundle_name(base_name, top_locale)]
                bundle.set_resources_root(root)
            except KeyError:
                bundle = _new_bundle(base_name, top_locale, self._name.split(".")[-1], root=root, bundle_type=type(self))
            self._set_parent(bundle)

    def get(self, key: str, *args, **kwargs) -> str:
        """
        Gets an object from the BasicResourceBundle.
        :param key: The key of the desired object
        :type key: str
        :return: The object
        :rtype: str
        """
        obj = self._handle_get_object(key, *args, **kwargs)
        if obj is None:
            if self._parent is not None:
                obj = self._parent.get(key, *args, **kwargs)
            if obj is None:
                raise NotInResourceBundleError(self._name, key)
        return obj

    def get_name(self) -> str:
        """
        Getter for the name of this BasicResourceBundle.
        :return: The name
        :rtype: str
        """
        return self._name

    def get_keys(self) -> List[str]:
        """
        Gets the currently loaded keys.
        :return: The keys
        :rtype: List[str]
        """
        return list(self._lookup.keys())

    def get_values(self) -> List[str]:
        """
        Gets the currently loaded values.
        :return: The values
        :rtype: List[str]
        """
        return list(self._lookup.values())

    def get_all_keys(self) -> List[str]:
        """
        Gets all keys from this BasicResourceBundle and its parents.
        Due to casting to set the order of the keys can vary.
        :return: The keys
        :rtype: List[str]
        """
        if self._parent is not None:
            return list(set(self.get_keys() + self._parent.get_all_keys()))
        else:
            return self.get_keys()

    def get_all_values(self) -> List[str]:
        """
        Gets all values from this BasicResourceBundle and its parents.
        Due to casting to set the order of the values can vary.
        Usage of this method is not encouraged.
        :return: The keys
        :rtype: List[str]
        """
        if self._parent is not None:
            return list(set(self.get_values() + self._parent.get_all_values()))
        else:
            return self.get_values()

    def __str__(self):
        return "<{} - '{}'>".format(self.__class__.__name__, self._name)

    def __repr__(self):
        return str(self)


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
    return _new_bundle(base_name, locale_, _STANDARD_FILE_EXTENSION, root=root)


def _to_resource_name(bundle_name: str, format_: str) -> str:
    """
    Converts the BasicResourceBundle name into the corresponding resource path.
    :param bundle_name: The specific name of the BasicResourceBundle
    :type bundle_name: str
    :param format_: The format of this BasicResourceBundle (file extension)
    :type format_: str
    :return: The resource name
    :rtype: str
    """
    return bundle_name + "." + format_


def _to_bundle_name(base_name: str, locale_: Locale) -> str:
    """
    Generates the bundle name for a BasicResourceBundle.
    :param base_name: The base name of the BasicResourceBundle
    :type base_name: str
    :param locale_: The locale to use for generating the name
    :type locale_: ..util.Locale
    :return: The name of the BasicResourceBundle
    :rtype: str
    """
    return base_name + locale_.get_delim() + locale_.to_string() if locale_ != ROOT_LOCALE else base_name


def _new_bundle(base_name: str, locale_: Locale, format_: str, root: str = ".",
                bundle_type: Type[RawResourceBundle] = RawResourceBundle
                ) -> RawResourceBundle:
    """
    Creates a new ResourceBundle.
    :param base_name: The base name of this ResourceBundle
    :type base_name: str
    :param locale_: The locale for this ResourceBundle
    :type locale_: ..util.Locale
    :param format_: The format (file extension)
    :type format_: str
    :param root: The resources root directory path
    :type root: str
    :param bundle_type: The type of the ResourceBundle
    :type bundle_type: RawResourceBundle
    :return: The new ResourceBundle
    :rtype: BasicResourceBundle
    """
    if locale_ is None:
        return _new_bundle(base_name=base_name, locale_=ROOT_LOCALE, format_=format_,
                           root=root, bundle_type=bundle_type)
    if type(locale_) is str:
        locale_ = from_iso(str(locale_))
    try:
        bundle = bundle_type(_to_resource_name(_to_bundle_name(base_name, locale_), format_), root=root)
        bundle.generate_parent_chain(base_name, locale_, root=root)
        return bundle
    except FileNotFoundError:
        if locale_ != ROOT_LOCALE:
            return _new_bundle(base_name, locale_.get_top_locale(), format_, root=root, bundle_type=bundle_type)
        else:
            raise MissingResourceBundleError(_to_bundle_name(base_name, locale_))
