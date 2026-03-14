from io import UnsupportedOperation

import domain.classes as domain
import translator.workers as workers

def print_separator():
    print("------------------")

def console_intro():
    print_separator()
    print("Console dictionary by Gabri")
    print()
    print("1) Aggiungi una nuova parola")
    print("2) Cerca una traduzione")
    print("3) Cerca con wildcard")
    print("4) Stampa tutto il dizionario")
    print("5) Exit")
    print()
    return int(input("Your choice --> "))

"""Add a new translation to the dictionary"""
def _add_translation(dictionary: domain.Dictionary) -> bool:
    print("This will add a new translation to the dictionary")
    alien = input("Insert alien word to translate (no spaces, unicode): ")
    if not domain.is_valid_input(alien):
        print("Invalid input")
        return False

    italian = input("Insert italian word: ")
    if not domain.is_valid_input(italian):
        print("Invalid input")
        return False

    try:
        dictionary.import_from_strings(alien, italian)
        print("New term added to dictionary successfully")
    except UnsupportedOperation as e:
        print("Tried to assign a new translation to a pre-existing translation, currently unsupported")
        return False

    return True

def _search_translation(dictionary: domain.Dictionary):
    alien = input("Insert alien word to translate (no spaces, unicode): ")
    if not domain.is_valid_input(alien):
        print("Invalid input")
        return False

    if dictionary.exists(alien):
        print(f"Translations for {alien} are: {dictionary.get_translation(alien).italian}")
        return True

    print(f"No translation for {alien}")
    return False

def _search_wildcard(dictionary: domain.Dictionary):
    pass        # TODO: Implement in program logic

def _print_dictionary(dictionary: domain.Dictionary):
    dictionary.print_all()

def _main():
    print("Hello world")

    worker = workers.TranslatorWorker("../dictionary.txt")
    translations_loaded = worker.load()
    print(translations_loaded)
    print(f"There are {translations_loaded.multiple_translations} multiple translations and {translations_loaded.single_translations} single translations")

    while True:
        print(translations_loaded)
        choice = console_intro()
        if choice <= 0 or choice > 5:
            print("Il valore inserito non va bene")
            pass

        # Main menu implementation
        elif choice == 1:
            r = _add_translation(translations_loaded)
            if r:
                worker.write(translations_loaded)   # save only if there are modifications
        elif choice == 2:
            _search_translation(translations_loaded)
        elif choice == 3:
            _search_wildcard(translations_loaded)
        elif choice == 4:
            _print_dictionary(translations_loaded)
        elif choice == 5:
            quit()

if __name__ == "__main__":
    _main()