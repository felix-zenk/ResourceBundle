import re
import warnings


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
    _var_types = {"s": str, "i": int, "f": float, "b": bytes}
    _var_types_pattern = "{([sifb]):(.+)}"

    def __init__(self):
        """
        Class for IO interaction, loads lists from an input file.
        """
        super(ListReader, self).__init__()

    def load(self, file_path: str) -> None:
        """
        Loads lists from a file and ignores empty lines
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
                    if value.endswith("]") and value.startswith("["):
                        value = value[1:-1]
                    if ", " in value:
                        values = [val for val in value.split(", ")]
                    else:
                        values = [val for val in value.split(",")]
                    for i in range(len(values)):
                        if values[i] == "{None}":
                            values[i] = None
                            continue
                        if re.match(self._var_types_pattern, values[i]):
                            if re.search(self._var_types_pattern, values[i]).group(1).lower() == "i":
                                if re.search(self._var_types_pattern, values[i]).group(2).lower() == "true":
                                    values[i] = True
                                    continue
                                if re.search(self._var_types_pattern, values[i]).group(2).lower() == "false":
                                    values[i] = False
                                    continue
                            try:
                                if re.search(self._var_types_pattern, values[i]).group(1).lower() == "b":
                                    values[i] = bytes(re.search(self._var_types_pattern, values[i]).group(2), "utf-8")
                                    continue
                                else:
                                    values[i] = self._var_types[re.search(self._var_types_pattern, values[i]).group(1)](
                                        re.search(self._var_types_pattern, values[i]).group(2))
                            except ValueError:
                                warnings.warn("Formatted value of '" + values[i] +
                                              "' is malformed! Failed to convert to type " +
                                              str(self._var_types[re.search(
                                                  self._var_types_pattern, values[i]).group(1)]))
                        else:
                            continue
                except IndexError:
                    raise LookupError("Malformed file: '" + file_path + "'")
                if key not in self._lookup.keys():
                    self._lookup[key] = values
                else:
                    raise LookupError("Duplicate key '" + key + "' in file '" + file_path + "'")
