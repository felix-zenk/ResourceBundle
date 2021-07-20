import os


class SimpleReader:
    def __init__(self):
        self._lookup = {}

    def load(self, file_path):
        with open(file_path) as f:
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

    def get(self):
        return self._lookup
