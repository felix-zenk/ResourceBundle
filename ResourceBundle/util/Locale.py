class Locale:

    def __init__(self, language: str = None, country: str = None, variant: str = None,
                 use_locale_module: bool = False):
        """
        Class that represents a locale.
        :param language: The language code
        :type language: str
        :param country: The country code
        :type country: str
        :param variant: The variant code
        :type variant: str
        :param use_locale_module: Whether or not to ignore the other params
                                  and use the locale defined through the locale module.
                                  Use locale.setlocale(locale.LC_ALL, "language") to set the used locale
        :type use_locale_module: bool
        """
        if use_locale_module:
            import locale
            params = locale.getlocale()[0].split("_")
            for param in params[:]:
                if len(param) != 2:  # only support 2 char codes
                    params = []  # module is unusable
            if len(params) > 1:
                self.__init__(language=params[0], country=params[1])
                return
            elif len(params) == 1:
                self.__init__(language=params[0])
                return
            else:
                from warnings import warn
                warn("locale module could not be used! Used locale: " + str(locale.getlocale()))
        self._delim = "_"
        if language is None or language == "":
            self._language = ""
        else:
            if len(language) == 2:
                self._language = language
            else:
                raise ValueError("Invalid language: " + language)
        if country is None or country == "":
            self._country = ""
        else:
            if len(country) == 2:
                self._country = country.upper()
            else:
                raise ValueError("Invalid country: " + country)
        if variant is None or variant == "":
            self._variant = ""
        else:
            self._variant = variant

    def get_language(self) -> str:
        """
        Getter for the language.
        :return: The language code
        :rtype: str
        """
        return self._language

    def get_country(self) -> str:
        """
        Getter for the country.
        :return: The country code
        :rtype: str
        """
        return self._country

    def get_variant(self) -> str:
        """
        Getter for the variant.
        :return: The variant code
        :rtype: str
        """
        return self._variant

    def get_delim(self) -> str:
        """
        Getter for the delimiter.
        :return: The delimiter
        :rtype: str
        """
        return self._delim

    def set_delim(self, delim: str) -> None:
        """
        Setter for the delimiter.
        Usage of this method is discouraged.
        :param delim: The new delimiter
        :type delim: str
        :return: Nothing
        :rtype: None
        """
        self._delim = delim

    def to_string(self) -> str:
        """
        Returns a string representation of this locale.
        :return: The string representation
        :rtype: str
        """
        string = ""
        if self._language == "" and self._country == "" and self._variant == "":
            return "ROOT"

        if self._variant != "":
            string += self._language + self._delim + self._country + self._delim + self._variant
        elif self._country != "":
            string += self._language + self._delim + self._country
        else:
            string += self._language
        return string

    def __str__(self) -> str:
        """
        Returns a string representation of this locale.
        :return: The string representation
        :rtype: str
        """
        return self.to_string()

    def __eq__(self, other) -> bool:
        """
        Checks if this Locale is equal to another Locale.
        :param other: The other Locale
        :type other: Locale
        :return: Whether this Locale is equal to the other Locale
        :rtype: bool
        """
        return (self._language == other.get_language() and self._country == other.get_country()
                and self._variant == other.get_variant())

    def __ne__(self, other) -> bool:
        """
        Checks if this Locale is not equal to another Locale.
        :param other: The other Locale
        :type other: Locale
        :return: Whether this Locale is different from the other Locale
        :rtype: bool
        """
        return not self == other

    def get_top_locale(self):
        """
        Returns the top Locale of this Locale.
        :return: The top locale
        :rtype: Locale
        """
        if self._country == "" and self._variant == "":
            if self._language != "":
                return ROOT_LOCALE
            else:
                return None

        if self._variant != "":
            if self._country != "":
                return Locale(language=self._language, country=self._country)
            else:
                return Locale(language=self._language)
        else:
            return Locale(language=self._language)


def new_locale(language: str = None, country: str = None, variant: str = None,
               use_locale_module: bool = False) -> Locale:
    """
    Instantiates a new Locale
    :param language: The language code
    :type language: str
    :param country: The country code
    :type country: str
    :param variant: The variant code
    :type variant: str
    :param use_locale_module: Whether or not to ignore the other params
                              and use the locale defined through the locale module.
                              Use locale.setlocale(locale.LC_ALL, "language") to set the used locale
    :type use_locale_module: bool
    :return: The new Locale object
    :rtype: Locale
    """
    return Locale(language, country, variant, use_locale_module)


def from_iso(iso_str: str):
    """
    Translates a locale string into a locale
    !Experimental!
    :param iso_str: The locale string
    :type iso_str: str
    :return: The new Locale
    :rtype: Locale
    """
    parts = iso_str.split("_")
    if len(parts) == 1:
        return new_locale(language=parts[0])
    elif len(parts) == 2:
        return new_locale(language=parts[0], country=parts[1])
    elif len(parts) == 3:
        return new_locale(language=parts[0], country=parts[1], variant=parts[2])
    else:
        return ROOT_LOCALE


# Constants
ROOT_LOCALE = Locale(language="", country="", variant="")  # The root Locale
