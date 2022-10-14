# ResourceBundle

[![PyPI-Versions](https://img.shields.io/pypi/pyversions/ResourceBundle)](https://pypi.org/project/ResourceBundle)
[![PyPI version](https://badge.fury.io/py/ResourceBundle.svg)](https://pypi.org/project/ResourceBundle)
[![License](https://img.shields.io/github/license/felix-zenk/onboardapis)](https://github.com/felix-zenk/onboardapis/blob/main/LICENSE)


ResourceBundle is a module that manages internationalization of string resources.
It is inspired by javas ResourceBundle and accepts the same format as a java PropertyResourceBundle.

---
### Installation

The ResourceBundle module can be downloaded from [PyPI](https://pypi.org/project/ResourceBundle):

```bash
$  python -m pip install ResourceBundle
```

### Usage

Each translation file you provide should have key-value pairs inside:
```
# This is a comment

key=value
another_key=Another value
```

Save the files of your ResourceBundle in the following structure and file name format:
```
./
├── BundleName.properties  # Recommended as a fallback
├── BundleName_languageCode_countryCode_variant.properties
└── ...
```

For example:
```
./
├── Strings.properties
├── Strings_en.properties
├── Strings_en_US.properties
└── ...
```

The recommended way to get a ResourceBundle instance is by using ``ResourceBundle.get_bundle(name, locale)``.
This function also provides support for pythons builtin ``locale`` moudule.

```python
import locale
import ResourceBundle

bundle = ResourceBundle.get_bundle("Strings", "en")
bundle = ResourceBundle.get_bundle("Strings", locale.getlocale())

# It is now possible to get a resource with the get() method
bundle.get("key")
```

If the key could not be found in the ResourceBundle the parent ResourceBundles will be searched
until a matching key was found, or it is determined that the key is not present in any parent ResourceBundle.

---

#### Accessing the available key-value items in your code:

ResourceBundles can be converted into dict objects with ``dict(bundle)``.
If you want to include the whole chain to get every accessible key and value, just iterate over the bundles parent.

```python
import ResourceBundle

bundle = ResourceBundle.get_bundle("Strings")

everything = dict(bundle)
while bundle.parent is not None:
    bundle = bundle.parent
    everything.update(dict(bundle))
```
