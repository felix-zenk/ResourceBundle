class Locale:
    """
    Class that represents a locale
    """
    def __init__(self, language: str = None, country: str = None, script: str = None, variant: str = None, **kwargs):
        """
        Initializes a new Locale
        :param language: The language code
        :type language: str
        :param country: The country code
        :type country: str
        :param script: The script code
        :type script: str
        :param variant: The variant code
        :type variant: str
        """
        self._delim = "_"
        if language is None:
            self._language = ""
        else:
            if len(language) == 2:
                self._language = language
            else:
                raise ValueError("Invalid language: " + language)
        if country is None:
            self._country = ""
        else:
            if len(country) == 2:
                self._country = country.upper()
            else:
                raise ValueError("Invalid country: " + country)
        if script is None:
            self._script = ""
        else:
            if len(script) > 0:  # TODO what's the length?
                self._script = script
            else:
                raise ValueError("Invalid script: " + script)
        if variant is None:
            self._variant = ""
        else:
            if len(variant) > 0:  # TODO what's the length?
                self._variant = variant
            else:
                raise ValueError("Invalid variant: " + variant)

    def get_language(self):
        """
        Getter for the language
        :return: The language code
        :rtype: str
        """
        return self._language

    def get_country(self):
        """
        Getter for the country
        :return: The country code
        :rtype: str
        """
        return self._country

    def get_script(self):
        """
        Getter for the script
        :return: The script code
        :rtype: str
        """
        return self._script

    def get_variant(self):
        """
        Getter for the variant
        :return: The variant code
        :rtype: str
        """
        return self._variant

    def get_delim(self):
        """
        Getter for the delimiter
        :return: The delimiter
        :rtype: str
        """
        return self._delim

    def set_delim(self, delim: str):
        """
        Setter for the delimiter
        :param delim: The new delimiter
        :type delim: str
        :return: Nothing
        :rtype: None
        """
        self._delim = delim

    def to_string(self):
        """
        Returns a string representation of this locale
        :return: The string representation
        :rtype: str
        """
        if self._language == "" and self._country == "" and self._variant == "":
            return ""
        string = ""

        if self._script != "":
            if self._variant != "":
                string += self._language + self._delim + self._script + self._delim \
                          + self._country + self._delim + self._variant
            elif self._country != "":
                string += self._language + self._delim + self._script + self._delim + self._country
            else:
                string += self._language + self._delim + self._script
        else:
            if self._variant != "":
                string += self._language + self._delim + self._country + self._delim + self._variant
            elif self._country != "":
                string += self._language + self._delim + self._country
            else:
                string += self._language
        return string

    def __str__(self):
        """
        Returns a string representation of this locale
        :return: The string representation
        :rtype: str
        """
        return self.to_string()

    def get_top_locale(self):
        """
        Returns the top locale of this locale
        :return: The top locale
        :rtype: Locale
        """
        if self._language != "":
            pass

        return ROOT  # TODO get right locale


# Constants
ROOT = Locale("", "", "", "")
