class MissingResourceBundleError(RuntimeError):
    def __init__(self):
        super(MissingResourceBundleError, self).__init__("This resource bundle does not exist")


class NotInResourceBundleError(LookupError):
    def __init__(self, bundle_name: str, key: str):
        super(NotInResourceBundleError, self).__init__("Can't find resource for bundle {}, key {}"
                                                       .format(bundle_name, key))
