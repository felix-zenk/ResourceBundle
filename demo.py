import locale

from ResourceBundle import get_bundle, ResourceBundle, get_list_bundle
from ResourceBundle.util.Locale import Locale, ROOT


def write_to_file(filename_without_extension, data):
    with open(filename_without_extension + ".properties", "w", encoding="utf-8") as f:
        f.write(data)


def generate_bundle(name: str) -> None:
    write_to_file(name, "# This is a comment\n" +
                  "replace_key=This is the {second_key} and this is a custom value: {}\n" +
                  "this_is_a_key=This is its value\n" +
                  "second_key=second value\n" +
                  "key_only_in_root=And nowhere else\n")
    write_to_file(name + "_de", "this_is_a_key=Das ist sein Wert\n" +
                  "second_key=Zweiter Wert\n")
    write_to_file(name + "_fr", "this_is_a_key=C'est sa valeur\n" +
                  "second_key=deuxième valeur\n")


def demo(bundle_: ResourceBundle, key: str):
    print("Key: {:<20} - Value: {}".format(key, bundle_.get(key)))


def demo_format(bundle_, key):
    print("Key: {:<20} - Value: {}".format(key, bundle_.get_formatted(key, "Custom stuff")))


def main():
    # Initialization
    generate_bundle("Strings")

    # Demonstration
    bundle = get_bundle("Strings", ROOT)
    print("\nCurrent bundle: " + bundle.get_name())
    demo(bundle, "this_is_a_key")
    demo(bundle, "second_key")
    demo(bundle, "key_only_in_root")
    demo_format(bundle, "replace_key")

    bundle = get_bundle("Strings", Locale(language="fr"))
    print("\nCurrent bundle: " + bundle.get_name())
    demo(bundle, "this_is_a_key")
    demo(bundle, "second_key")
    demo(bundle, "key_only_in_root")
    demo_format(bundle, "replace_key")

    bundle = get_bundle("Strings", Locale(language="de", country="de"))
    print("\nCurrent bundle: " + bundle.get_name())
    demo(bundle, "this_is_a_key")
    demo(bundle, "second_key")
    demo(bundle, "key_only_in_root")
    demo_format(bundle, "replace_key")

    locale.setlocale(locale.LC_ALL, "it")
    print("\nTrying to use your locale: " + str(locale.getlocale()))
    bundle = get_bundle("Strings", Locale(use_locale_module=True))
    print(("Current bundle: " + bundle.get_name()) if bundle.get_name() != "Strings.properties"
          else "Your Locale is not in the BasicResourceBundle! Fallback on: " + bundle.get_name())
    demo(bundle, "this_is_a_key")
    demo(bundle, "second_key")
    demo(bundle, "key_only_in_root")


def main_list():
    print("\n\nList bundles also exist!")
    write_to_file("Lists", "key=[This is a value, and this too, great!]")
    bundle = get_list_bundle("Lists", ROOT)
    demo(bundle, "key")


if __name__ == '__main__':
    main()
    main_list()
