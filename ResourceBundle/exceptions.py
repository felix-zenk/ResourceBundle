"""
Module that contains all exceptions that are part of the ResourceBundle package.
"""


class ResourceBundleError(LookupError):
    """Base class for all exceptions in the ResourceBundle module."""


class MalformedResourceBundleError(ResourceBundleError):
    """Error that indicates that a ResourceBundle is malformed."""


class NotInResourceBundleError(ResourceBundleError):
    """Error that is raised when a key could not be found in a ResourceBundle."""

    def __init__(self, bundle_name: str, key: str) -> None:
        """Initialize a new NotInResourceBundleError.

        :param str bundle_name: The name of the ResourceBundle
        :param str key: The key that could not be found
        """
        super(NotInResourceBundleError, self).__init__(f"Can't find key {key} in bundle {bundle_name}!")
