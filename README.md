# ResourceBundle

[![PyPI-Versions](https://img.shields.io/pypi/pyversions/ResourceBundle)](https://pypi.org/project/ResourceBundle)
[![PyPI version](https://badge.fury.io/py/ResourceBundle.svg)](https://pypi.org/project/ResourceBundle)
[![Build package](https://github.com/felix-zenk/ResourceBundle/actions/workflows/build.yaml/badge.svg)](https://github.com/felix-zenk/ResourceBundle/actions/workflows/build.yaml)
[![License](https://img.shields.io/github/license/felix-zenk/onboardapis)](https://github.com/felix-zenk/ResourceBundle/blob/main/LICENSE)

ResourceBundle is a package that manages internationalization / localization (i18n / l10n) of string resources.
It is inspired by Java's ResourceBundle and accepts the same format as a Java ``PropertyResourceBundle``.

> **Note:** ResourceBundle is not the pythonic way of internationalization / localization.
> This package is only intended to be used if you *absolutely have* to work with ResourceBundle files
> or need a quick working way when porting from Java.
>
> For information on how to do internationalization in python,
> see the [official documentation](https://docs.python.org/3/library/gettext.html).
> You can use the [`ResourceBundle.Converter.to_gettext()`](#gettext)
> method to convert your ResourceBundle files to gettext `po` files.

---
### Installation

The ResourceBundle module can be downloaded from [PyPI](https://pypi.org/project/ResourceBundle):

```bash
# Linux / macOS
$  python3 -m pip install ResourceBundle

# Windows
>  py -m pip install ResourceBundle
```

### Usage

Assuming you come from Java, you are probably familiar with the ResourceBundle file format.
If not, you can read about it
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

The ResourceBundle module can convert ResourceBundle files to gettext `pot` / `po` files.
This can be done by using the ``ResourceBundle.Converter.to_gettext()`` method.

```python
from ResourceBundle import Converter

# convert all .properties files in the current directory to .po files
Converter.to_gettext(".", ".")
```

Note however that this step is obsolete if you are using ``gettext`` properly
as this will include automatically extracting strings from your source code with the help of a library like
[Babel](https://babel.pocoo.org/en/latest/) with its [pybabel](https://babel.pocoo.org/en/latest/cmdline.html) tool.
The function is only intended as a head start to keep existing translations.
