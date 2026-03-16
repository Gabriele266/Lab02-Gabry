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

"""Add a new translation to the dictionary
Also accepts multiple translations, separated by comma
"""
def _add_translation(dictionary: domain.Dictionary) -> bool:
    print("This will add a new translation to the dictionary")
    alien = input("Insert alien word to translate (no spaces, unicode): ")
    if not domain.is_valid_input(alien):
        print("Invalid input")
        return False

    italian_terms = input("Insert italian word (or list of comma-separated): ")        # can be a single italian word or a list separated by comma
    if "," in italian_terms:
        italian_terms = italian_terms.split(",")
    else:
        italian_terms = [italian_terms]

    # validate all terms in the italian list
    for term in italian_terms:
        if domain.is_valid_input(term):
            dictionary.import_from_strings(alien, term)
        else:
            print(f"Invalid italian term {term} for {alien}")
            return False

    print(f"New alien term added to dictionary with {len(italian_terms)} italian terms associated")

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
    w = input("Insert wildcard word to search for (max 1 ?): ")

    try:
        results = dictionary.search_wildcard(w)

        print()

        if len(results) == 0:
            print(f"No results for {w}")
            return

        print("Your search results:")
        for key in results.keys():
            print(f"{key}: {results[key].italian}")

        print()
    except ValueError as e:
        print(f"Invalid wildcard inserted {w}")

    pass

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