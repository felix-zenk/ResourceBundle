import re

from os.path import exists, isfile
from typing import List

from ..util.Locale import Locale, ROOT
from ..util.readers import SimpleReader
from ..exceptions import NotInResourceBundleError, MissingResourceBundleError


class ResourceBundle:
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
        self._reader = SimpleReader()
        self.set_resources_root(root)  # Set correct root
        if path is not None:
            self._name = path
            self._load(path)
        else:
            self._name = "INVALID"

    def _load(self, path: str) -> None:
        """
        Loads keys and values into this ResourceBundle instance.
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

    def _handle_get_object(self, key) -> object:
        """
        Searches the given key in this ResourceBundle and returns its value if found, else None.
        :param key:
        :type key:
        :return:
        :rtype:
        """
        try:
            return self._lookup[key]
        except KeyError:
            return None

    def _set_parent(self, parent) -> None:
        """
        Sets the parent for this bundle.
        :param parent: The new parent
        :type parent: ResourceBundle
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
        Generates the parent chain for this ResourceBundle.
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
        self._cached_bundles[_to_bundle_name(base_name, locale_)] = self
        if top_locale is None:
            return
        else:
            try:
                bundle = self._cached_bundles[_to_bundle_name(base_name, top_locale)]
                bundle.set_resources_root(root)
            except KeyError:
                bundle = get_bundle(base_name, top_locale, root=root)
            self._set_parent(bundle)

    def __str__(self):
        return "<{} - '{}'>".format(self.__class__.__name__, self._name)

    def format(self, string: str, *replacements) -> str:
        """
        Replaces {} with replacements.
        If fewer replacements than brackets in the string get supplied the corresponding brackets will not be replaced!
        If more replacements than brackets in the string get supplied the remaining replacements will be ignored.
        :param string: The string that will be formatted
        :type string: str
        :param replacements: All the replacements for every {}
        :type replacements: *args: str
        :return: The formatted string
        :rtype: str
        """
        if type(replacements[0]) is list:
            replacements = replacements[0]
        elif type(replacements[0]) is tuple:
            replacements = [elem for elem in replacements[0]]
        partial_strings = string.split("{}")
        resulting_string = ""
        for i in range(len(partial_strings) - 1):
            try:
                resulting_string += partial_strings[i] + replacements[i]
            except IndexError:
                resulting_string += partial_strings[i] + "{}"  # No replacement left for this bracket
        return resulting_string + partial_strings[-1]

    def autoformat(self, string: str, *replacements) -> str:
        """
        Replaces {} like python f-String
        :param string: The string that will be formatted
        :type string: str
        :param replacements: Optional replacements in case {} occurs in the string
        :type replacements: *args: str
        :return: The formatted string
        :rtype: str
        """
        if string is None:
            return None
        if len(replacements) == 1 and type(replacements[0]) is tuple:
            replacements = replacements[0]
        replacements_needed = re.findall(r"{}", string)
        replacements_auto_searched = re.findall(r"{([.\w\d]+)}", string)
        if replacements_needed is not None and len(replacements_needed) > len(replacements):
            return None  # Too few params
        result = self.format(string, replacements)
        values = [self.get(key) for key in replacements_auto_searched]
        return self.format(re.sub(r"{[.\w\d]+}", "{}", result), values)

    def get(self, key: str) -> str:
        """
        Gets an object from the ResourceBundle.
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
                raise NotInResourceBundleError(self._name, key)
        return obj

    def get_formatted(self, key: str, *replacements) -> str:
        """
        Gets an object from the ResourceBundle and automatically formats the result
        {} gets replaced by the *replacements
        {another_key} searches this ResourceBundle for that key and substitutes it with its value
        :param key: The key of the object
        :type key: str
        :param replacements: The replacements for empty curly brackets
        :type replacements: *args:str
        :return: The formatted object
        :rtype: str
        """
        if len(replacements) > 0:
            return self.autoformat(self.get(key), replacements)
        else:
            return self.autoformat(self.get(key))

    def get_name(self) -> str:
        """
        Getter for the name of this ResourceBundle.
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
        Gets all keys from this ResourceBundle and its parents.
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
        Gets all values from this ResourceBundle and its parents.
        Due to casting to set the order of the values can vary.
        Usage of this method is not encouraged.
        :return: The keys
        :rtype: List[str]
        """
        if self._parent is not None:
            return list(set(self.get_values() + self._parent.get_all_values()))
        else:
            return self.get_values()


def get_bundle(base_name: str, locale_: Locale = None, root: str = ".") -> ResourceBundle:
    """
    Gets a specific ResourceBundle.
    :param base_name: The name of the ResourceBundle
    :type base_name: str
    :param locale_: The locale
    :type locale_: ..util.Locale
    :param root: The resources root directory path
    :type root: str
    :return: The ResourceBundle
    :rtype: ResourceBundle
    """
    return _new_bundle(base_name, locale_, "properties", root=root)


def _to_resource_name(bundle_name: str, format_: str) -> str:
    """
    Converts the ResourceBundle name into the corresponding resource path.
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
    Generates the bundle name for a ResourceBundle.
    :param base_name: The base name of the ResourceBundle
    :type base_name: str
    :param locale_: The locale to use for generating the name
    :type locale_: ..util.Locale
    :return: The name of the ResourceBundle
    :rtype: str
    """
    return base_name + locale_.get_delim() + locale_.to_string() if locale_ != ROOT else base_name


def _new_bundle(base_name: str, locale_: Locale, format_: str, root: str = ".") -> ResourceBundle:
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
    :return: The new ResourceBundle
    :rtype: ResourceBundle
    """
    try:
        bundle = ResourceBundle(_to_resource_name(_to_bundle_name(base_name, locale_), format_), root=root)
        bundle.generate_parent_chain(base_name, locale_, root=root)
        return bundle
    except FileNotFoundError:
        if locale_ != ROOT:
            return _new_bundle(base_name, locale_.get_top_locale(), format_, root=root)
        else:
            raise MissingResourceBundleError(_to_bundle_name(base_name, locale_))
