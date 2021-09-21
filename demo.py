import locale

from ResourceBundle import get_bundle, ResourceBundle, get_list_bundle, Locale


def write_to_file(filename_without_extension, data):
    with open(filename_without_extension + ".properties", "w", encoding="utf-8") as f:
        f.write(data)


def generate_bundle(name: str) -> None:
    write_to_file(name, "# This is a comment\n" +
                  "replace_key=This is the {second_key} and this is a custom value: {}\n" +
                  "this_is_a_key=This is its value\n" +
                  "second_key=second value\n" +
                  "key_only_in_root=And nowhere else\n" +
                  "inception1=This {inception2} keys!\n" +
                  "inception2=sentence is {inception3} multiple\n" +
                  "inception3=split across\n")
    write_to_file(name + "_de", "this_is_a_key=Das ist sein Wert\n" +
                  "second_key=Zweiter Wert\n" +
                  "replace_key=Das hier ist '{second_key}' und ein eigener Wert: {}\n" +
                  "inception1=Dieser {inception2} aufgeteilt!\n" +
                  "inception2=Satz {inception3} Schlüssel\n" +
                  "inception3=ist auf mehrere\n")
    write_to_file(name + "_fr", "this_is_a_key=C'est sa valeur\n" +
                  "second_key=deuxième valeur\n")


def demo(bundle_: ResourceBundle, key: str):
    print("Key: {:<20} - Value: {}".format(key, bundle_.get(key)))


def demo_format(bundle_, key):
    print("Key: {:<20} - Value: {}".format(key, bundle_.get_formatted(key, "Custom stuff")))


def demo_recursive_format(bundle_, key):
    print("Key: {:<20} - Value: {}".format(key, bundle_.get_formatted(key)))


def main():
    # Initialization
    generate_bundle("Strings")

    # Demonstration
    for bundle in [get_bundle("Strings", Locale.ROOT_LOCALE),
                   get_bundle("Strings", Locale.new_locale(language="fr")),
                   get_bundle("Strings", Locale.new_locale(language="de", country="de"))
                   ]:
        print("\nCurrent bundle: " + bundle.get_name())
        demo(bundle, "this_is_a_key")
        demo(bundle, "second_key")
        demo(bundle, "key_only_in_root")
        demo_format(bundle, "replace_key")
        demo_recursive_format(bundle, "inception1")

    # Integration of the locale module
    locale.setlocale(locale.LC_ALL, "it")
    print("\nTrying to use locale: " + str(locale.getlocale()))
    bundle = get_bundle("Strings", Locale.new_locale(use_locale_module=True))
    print(("Current bundle: " + bundle.get_name()) if bundle.get_name() != "Strings.properties"
          else "Your Locale is not in the BasicResourceBundle! Fallback on: " + bundle.get_name())
    demo(bundle, "this_is_a_key")
    demo(bundle, "second_key")
    demo(bundle, "key_only_in_root")
    demo_format(bundle, "replace_key")
    demo_recursive_format(bundle, "inception1")

    # List bundles
    print("\n\nList bundles also exist!")
    write_to_file("Lists", "key=[This is a value, {s:and this too}, {i:1}, {f:1}, {i:True}, {b:00🐧ff}]")
    bundle = get_list_bundle("Lists", Locale.ROOT_LOCALE)
    demo(bundle, "key")


if __name__ == '__main__':
    main()
