# ResourceBundle

ResourceBundle is a module that manages resource handling where different resources are needed depending on the current locale.
It is inspired by javas ResourceBundle and accepts a similar format as a java PropertyResourceBundle.

---
### Installing

The ResourceBundle module can be downloaded from [PyPI](https://pypi.org/project/ResourceBundle):

```bash
$  pip install ResourceBundle
```

[![PyPI version](https://img.shields.io/badge/pypi-v1.0.2-yellow)](https://pypi.org/project/ResourceBundle)

### Usage

Note: For a live demo look at [demo.py](https://github.com/felix-zenk/ResourceBundle/blob/main/demo.py)

Each translation file you provide should have key-value pairs inside:
```
# This is a comment

key=value
key2=Another value
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

You can access the resources through a ResourceBundle instance.
For creating a ResourceBundle it is recommended to use the function get_bundle()

```python
import ResourceBundle as rb
from ResourceBundle.util.Locale import Locale


bundle = rb.get_bundle("Strings", Locale("en"))

# It is now possible to get a resource with the get() method
bundle.get("key")
```

If the key could not be found in the ResourceBundle the module will look in its parent ResourceBundle until a matching key was found or it is determined that the key is not present in any parent file.
For example if the key 'hello' is present in a file called ```Strings.properties``` and the ResourceBundle.get("hello") was called the value of 'hello' from ```Strings.properties``` is returned.
Sometimes a key is missing in a file. If the key 'hello' does not exist in a file called ```Strings_en.properties``` ResourceBundle.get("hello") will then check ```Strings_en.properties``` and then look in ```Strings.properties```.

### Automatic substitution

If you have a key in your ResourceBundle that contains empty curly brackets ``{}`` you can get the key through the ``ResourceBundle.get_formatted()`` method and supply additional arguments.
The empty brackets will be replaced with the arguments in the order you provide them.
An exception are curly brackets with another key from the ResourceBundle inside it e.g. ``{another_key}``. That key gets automatically searched for in the ResourceBundle and inserted in those brackets.

```python
# key=This is a {}
bundle.get_formatted("key", "replacement")
# Returns the object that key refers to,
# but replaces {} with "replacement"
# -> "This is a replacement"

# key=me!
# another_key=The key is {key}
bundle.get_formatted("another_key")
# Returns the object that key refers to,
# but replaces {key} with the value of key
# -> "The key is me!"
```