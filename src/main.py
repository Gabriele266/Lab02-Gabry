import domain.classes
import translator.workers as workers

def _main():
    print("Hello world")

    translations_loaded = workers.TranslatorWorker("../dictionary.txt").load()
    print(translations_loaded)

    t2 = workers.TranslatorWorker("../foo.txt")
    translations_loaded.import_from_strings("erib", "URUB")
    t2.write(translations_loaded)

if __name__ == "__main__":
    _main()