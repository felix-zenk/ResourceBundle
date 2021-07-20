class MissingResourceBundleError(LookupError):

    def __init__(self, bundle_name):
        """
        Error that indicates that the ResourceBundle is missing.
        :param bundle_name: The name of the ResourceBundle
        :type bundle_name: str
        """
        super(MissingResourceBundleError, self).__init__("The ResourceBundle {} does not exist".format(bundle_name))


class NotInResourceBundleError(LookupError):

    def __init__(self, bundle_name: str, key: str):
        """
        Error that is raised when a key could not be found in a ResourceBundle.
        :param bundle_name: The name of the ResourceBundle
        :type bundle_name: str
        :param key: The key that could not be found
        :type key: str
        """
        super(NotInResourceBundleError, self).__init__("Can't find resource for bundle {}, key {}"
                                                       .format(bundle_name, key))
