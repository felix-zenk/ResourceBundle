import re
import warnings
from typing import Union


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
        def _parse(item: str) -> Union[str, int, float, bytes, None]:
            if item == "{None}":
                return None
            if re.match(self._var_types_pattern, item):  # If should be converted
                if re.search(self._var_types_pattern, item).group(1).lower() == "i":
                    if re.search(self._var_types_pattern, item).group(2).lower() == "true":
                        return True
                    if re.search(self._var_types_pattern, item).group(2).lower() == "false":
                        return False
                try:
                    if re.search(self._var_types_pattern, item).group(1).lower() == "b":
                        return bytes(re.search(self._var_types_pattern, item).group(2), "utf-8")
                    else:
                        return self._var_types[re.search(self._var_types_pattern, item).group(1)](
                            re.search(self._var_types_pattern, item).group(2))
                except ValueError:
                    warnings.warn("Formatted value of '" + item +
                                  "' is malformed! Failed to convert to type " +
                                  str(self._var_types[re.search(
                                      self._var_types_pattern, item).group(1)]))
            return item

        def _handle_list(value_: str) -> list:
            output = []
            while value_.endswith("\n") or value_.endswith("\r"):
                value_ = value_[:-1]
            if value_.strip() == '[]':
                return output
            if value_.startswith("[") and value_.endswith("]"):
                # list in list
                output.extend([_handle_list("["+val.split("]")[0]+"]") for val in value_[1:-1].split("[")[1:]])
                # remaining items in list
                output.extend(
                    [_parse(part.replace("\x1D", ",")) for part in
                     [val.strip() for val in value_[1:-1].replace("\\,", "\x1D").split(",")
                      if not (val.strip().startswith("[") or val.strip().endswith("]"))]
                     ])
            else:
                raise TypeError("Not a list! "+str(value_))
            return output

        # # # READ FILE # # #
        with open(file_path, encoding="utf-8") as f:
            lines = f.readlines()
        for line in lines:
            if not (line.strip().startswith('#') or line.strip() == ""):
                try:
                    key = line.split("=")[0].strip()
                    value = _handle_list(line.split("=")[1])
                except IndexError:
                    raise LookupError("Malformed file: '" + file_path + "'")
                except TypeError as te:
                    raise TypeError("Key '"+key+"' is not a valid list")
                if key not in self._lookup.keys():
                    self._lookup[key] = value
                else:
                    raise LookupError("Duplicate key '" + key + "' in file '" + file_path + "'")
