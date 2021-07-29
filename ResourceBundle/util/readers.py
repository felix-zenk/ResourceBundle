class SimpleReader:

    def __init__(self):
        """
        Class for IO interaction, loads key-value pairs from an input file.
        """
        self._lookup = {}

    def load(self, file_path: str) -> None:
        """
        Loads key-value pairs from a file and ignores empty lines
        and commented lines indicated through # at the start of a line.
        :param file_path: The file path
        :type file_path: str
        :return: Nothing
        :rtype: None
        """
        with open(file_path, encoding="utf-8") as f:
            lines = f.readlines()
        for line in lines:
            if not (line.strip().startswith('#') or line.strip() == ""):
                try:
                    key = line.split("=")[0].strip()
                    value = line.split("=")[1]
                    if value.endswith("\n"):
                        value = value[:-1]
                except IndexError:
                    raise LookupError("Malformed file: '" + file_path + "'")
                if key not in self._lookup.keys():
                    self._lookup[key] = value
                else:
                    raise LookupError("Duplicate key '" + key + "' in file '" + file_path + "'")

    def get(self) -> dict:
        """
        Getter for the dict loaded by load()
        :return: The dictionary of all key-value pairs from the loaded file
        :rtype: dict
        """
        return self._lookup


class ListReader(SimpleReader):
    def __init__(self):
        super(ListReader, self).__init__()

    def load(self, file_path: str) -> None:
        with open(file_path, encoding="utf-8") as f:
            lines = f.readlines()
        for line in lines:
            if not (line.strip().startswith('#') or line.strip() == ""):
                try:
                    key = line.split("=")[0].strip()
                    value = line.split("=")[1]
                    if value.endswith("\n"):
                        value = value[:-1]
                    if value.endswith("]") and value.startswith("["):
                        value = value[1:-1]
                    if ", " in value:
                        values = [val for val in value.split(", ")]
                    else:
                        values = [val for val in value.split(",")]
                except IndexError:
                    raise LookupError("Malformed file: '" + file_path + "'")
                if key not in self._lookup.keys():
                    self._lookup[key] = values
                else:
                    raise LookupError("Duplicate key '" + key + "' in file '" + file_path + "'")
