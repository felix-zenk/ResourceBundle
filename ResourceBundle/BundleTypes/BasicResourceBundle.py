import re

from ..util.Locale import Locale
from .RawResourceBundle import RawResourceBundle, _new_bundle


class BasicResourceBundle(RawResourceBundle):
    _cached_bundles = {}

    def __init__(self, path: str = None, root: str = "."):
        """
        Class that handles access to a resource across different locales.
        :param path: The path to the resource file
        :type path: str
        :param root: The resources root directory path
        :type root: str
        """
        super(BasicResourceBundle, self).__init__(path, root)

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
            raise TypeError("string must not be None")
        if len(replacements) == 1 and type(replacements[0]) is tuple:
            replacements = replacements[0]
        replacements_needed = re.findall(r"{}", string)
        replacements_auto_searched = re.findall(r"{([.\w\d]+)}", string)
        if replacements_needed is not None and len(replacements_needed) > len(replacements):
            return None  # Too few params
        result = replace(string, replacements)
        values = [self.get(key) for key in replacements_auto_searched]
        return replace(re.sub(r"{[.\w\d]+}", "{}", result), values)

    def get_formatted(self, key: str, *replacements) -> str:
        """
        Gets an object from the BasicResourceBundle and automatically formats the result
        {} gets replaced by the *replacements
        {another_key} searches this BasicResourceBundle for that key and substitutes it with its value
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


def replace(string: str, *replacements) -> str:
    """
    Replaces {} with replacements.
    len(replacements) must match the count of "{}" in the string
    :param string: The string that will be formatted
    :type string: str
    :param replacements: All the replacements for every {}
    :type replacements: *args: str
    :return: The formatted string
    :rtype: str
    """
    if string is None:
        raise TypeError("string must not be None")
    if type(replacements[0]) is list:
        replacements = replacements[0]
    elif type(replacements[0]) is tuple:
        replacements = [elem for elem in replacements[0]]
    partial_strings = string.split("{}")
    # Check for matching count
    if len(partial_strings) - 1 != len(replacements):
        raise TypeError("Argument count does not match! " +
                        str(len(partial_strings) - 1) +
                        "replacements are needed for the string \"" + string + "\", but " +
                        str(len(replacements)) + " were provided.")
    resulting_string = ""
    for i in range(len(partial_strings) - 1):
        resulting_string += partial_strings[i] + replacements[i]
    return resulting_string + partial_strings[-1]
