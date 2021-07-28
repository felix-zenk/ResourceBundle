# ResourceBundle

ResourceBundle is a module that manages resource handling where different resources are needed depending on the current locale.
It is inspired by javas ResourceBundle and accepts the same format as a java PropertyResourceBundle.

---
### Installing

The ResourceBundle module can be downloaded from [PyPI](https://pypi.org/project/ResourceBundle):

```bash
$  pip install ResourceBundle
```

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
# ResourceBundle

ResourceBundle is a module that manages resource handling where different resources are needed depending on the current locale.
It is inspired by javas ResourceBundle and accepts the same format as a java PropertyResourceBundle.

---
### Installing

The ResourceBundle module can be downloaded from PyPI:

```bash
$  pip install ResourceBundle
```

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
from ResouceBundle.util.Locale import Locale

bundle = rb.get_bundle("Strings", Locale("en"))
# It is now possible to get a resource with the get() method
bundle.get("key")
```

If the key could not be found in the ResourceBundle the module will look in its parent ResourceBundle until a matching key was found or it is determined that the key is not present in any parent file.
For example if the key 'hello' is present in a file called ```Strings.properties``` and the ResourceBundle.get("hello") was called the value of 'hello' from ```Strings.properties``` is returned.
Sometimes a key is missing in a file. If the key 'hello' does not exist in a file called ```Strings_en.properties``` ResourceBundle.get("hello") will then check ```Strings_en.properties``` and then look in ```Strings.properties```.
