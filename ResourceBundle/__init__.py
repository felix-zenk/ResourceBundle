"""
Module containing the implementation of the ResourceBundle
"""
from __future__ import annotations

from os import PathLike
from pathlib import Path
from typing import Sequence, KeysView

from .exceptions import NotInResourceBundleError, MalformedResourceBundleError

__version__ = "2.0.0"
__author__ = "Felix Zenk"
__email__ = "felix.zenk@web.de"


class _Parser(object):
    """
    A parser for the .properties file format.
    """
    @staticmethod
    def parse(file_path: Path) -> dict[str, str]:
        """
        Reads a ResourceBundle file and parses its contents

        :param Path file_path:
        :return: The contents of the file as a key-value dict
        """
        # I/O read
        print(file_path)
        with open(file_path, mode="r", encoding="utf-8") as f:
            lines = f.readlines()

        # parse
        mapping = dict()
        for line_no, line in enumerate(lines, start=1):
            if line.strip().startswith('#') or line.strip(' \n\r') == "":
                continue
            if "=" not in line:
                raise MalformedResourceBundleError(f"Malformed file: '{file_path}' (line {line_no})")

            key, *value = line.split("=")
            key = key.strip()
            value = '='.join(value).strip()

            if key not in mapping.keys():
                mapping[key] = value
            else:
                raise MalformedResourceBundleError(f"Duplicate key '{key}' in file '{file_path}' on line {line_no}")
        return mapping


class ResourceBundle(object):
    """
    A ResourceBundle manages internationalization of string resources
    """
    __cached_bundles = dict()

    __slots__ = ["_name", "_locale", "_parent", "_mapping"]

    def __init__(self, bundle_name: str, bundle_locale: str | None, *, path: str | PathLike = None) -> None:
        self._name: str = bundle_name
        self._locale: str | None = bundle_locale
        self._parent: ResourceBundle | None = self._get_parent_bundle()
        self._mapping: dict[str, str] = self._map(path=path)
        # Save self in cache
        self.__cached_bundles[self.name] = self

    @property
    def name(self) -> str:
        """
        Get the full name of the ResourceBundle
        """
        return f"{self._name}" if self._locale is None else f"{self._name}_{self._locale}"

    @property
    def parent(self) -> ResourceBundle:
        """
        Get the ResourceBundles parent ResourceBundle
        """
        return self._parent

    def _get_parent_bundle(self) -> ResourceBundle | None:
        # This is the root bundle
        if self._locale is None:
            return None

        # Cut one part off of the locale
        *parts, _ = self._locale.split("_")
        # If nothing is left set the locale to None else to the shortened locale
        parent_locale = '_'.join(parts) if len(parts) > 0 else None
        # If cached
        if self.__cached_bundles.get(parent_locale) is not None:
            return self.__cached_bundles.get(parent_locale)
        # Not cached, start building chain
        return ResourceBundle(self._name, parent_locale)

    def _map(self, path: str | PathLike | None) -> dict[str, str]:
        if path is None:
            path = Path()
        try:
            return _Parser.parse(Path(str(path)) / f"{self.name}.properties")
        except FileNotFoundError:
            return dict()

    def __getitem__(self, item) -> str:
        return self.get(item)

    def keys(self) -> KeysView[str, str]:
        """
        Return all keys present in this specific ResourceBundle
        """
        return self._mapping.keys()

    def get(self, item: str, __default: str = None) -> str:
        """
        Get the value of ``item`` from this or a parent ResourceBundle

        :param str item: The key to look up
        :param str __default: A default value that is returned if the key can't be found anywhere
        :return: The value
        """
        # found in mapping
        if self._mapping.get(item) is not None:
            return self._mapping.get(item)

        # ask parent
        if self._parent is not None:
            return self._parent.get(item)

        # is root bundle (has no parent)
        if __default is not None:
            return __default

        raise NotInResourceBundleError(self.name, item)


def get_bundle(bundle_name: str, locale: str | Sequence[str | str] = None) -> ResourceBundle:
    """
    Get a :class:`ResourceBundle` after parsing the locale

    :param str bundle_name: The bundles base name
    :param str | Sequence[str | str] locale: The locale as a string or from the locale module
    """
    # locale was supplied
    if locale is None:
        extracted_locale = None
    else:
        # simple string
        if isinstance(locale, str):
            extracted_locale = locale
        # locale from the locale module
        else:
            extracted_locale, _ = locale

    # bundle name
    extracted_name = bundle_name
    return ResourceBundle(extracted_name, extracted_locale)
