# ResourceBundle

[![PyPI-Versions](https://img.shields.io/pypi/pyversions/ResourceBundle)](https://pypi.org/project/ResourceBundle)
[![PyPI version](https://badge.fury.io/py/ResourceBundle.svg)](https://pypi.org/project/ResourceBundle)
[![License](https://img.shields.io/github/license/felix-zenk/onboardapis)](https://github.com/felix-zenk/onboardapis/blob/main/LICENSE)


ResourceBundle is a module that manages internationalization of string resources.
It is inspired by javas ResourceBundle and accepts the same format as a java PropertyResourceBundle.

> **Note:** ResourceBundle is not the python way of doing internationalization.
> This package is only intended to be used if you *absolutely have* to work with ResourceBundle files
> or need a quick working way when porting from java.
>
> For information on how to do internationalization in python,
> see the [official documentation](https://docs.python.org/3/library/gettext.html).
> You can use the `ResourceBundle.Converter.to_gettext()` method to convert your ResourceBundle files to gettext po files.

---
### Installation

The ResourceBundle module can be downloaded from [PyPI](https://pypi.org/project/ResourceBundle):

```bash
# linux / macOS
$  python3 -m pip install ResourceBundle

# windows
>  py -m pip install ResourceBundle
```

### Usage

Assuming you come from java, you are probably familiar with the ResourceBundle file format.
If not,you can read about it
[here](https://docs.oracle.com/en/java/javase/20/docs/api/java.base/java/util/PropertyResourceBundle.html).

Get a ResourceBundle instance is by using ``ResourceBundle.get_bundle(name, locale)``.

```python
import ResourceBundle

bundle = ResourceBundle.get_bundle("Strings", "en")

# It is now possible to get a resource with the get() method
bundle.get("key")
```

If the key could not be found in the ResourceBundle the parent ResourceBundles will be searched
until a matching key was found.
If the key is not present in any of its parents a ``ResourceBundle.exceptions.NotInResourceBundleError`` will be raised.

---

### gettext

The ResourceBundle module can convert ResourceBundle files to gettext pot / po files.
This can be done by using the ``ResourceBundle.Converter.to_gettext()`` function.

```python
from ResourceBundle import Converter

# convert all .properties files in the current directory to .po files
Converter.to_gettext(".", ".")
```

Note however that this step is obsolete if you are using gettext properly
as this will include automatically extracting strings from your source code.
The function is only intended as a head start to keep existing translations.
