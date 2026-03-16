import unittest
import src.translator.workers as workers

import src.domain.classes as domain
from src.domain.search import Wildcard


class TestCase(unittest.TestCase):
    def test_utils(self):
        self.assertIs(workers.set_to_str({"a"}), "a")

    def test_translation_validation(self):
       t = domain.Translation.validate("erum", "Mimmo")
       t2 = domain.Translation.validate("erum23432 3423", "Mimmo")
       t3 = domain.Translation.validate("ciao ciao", "Mimmo")
       t4 = domain.Translation.validate("neljä", "Mimmo")

       self.assertTrue(t)
       self.assertFalse(t2)
       self.assertFalse(t3, "Due parole separate da spazio non sono valide")
       self.assertFalse(domain.Translation.validate("/Ciao", "/Addio"))
       self.assertTrue(t4)
       self.assertRaises(ValueError, domain.Translation.__init__, "erum1234", "Mimmo", "Invalid constructor parameters should raise exception")
       to = domain.Translation("erum", "Mimmo")
       to2 = domain.Translation("erum", "Mimmo")
       self.assertEqual(to, to2)

    def test_multiple_translations(self):
        t = domain.Translation.from_multiple("urbit", ["mimmo", "lillo", "pizza"])

        self.assertFalse(t.isunique())
        self.assertTrue("mimmo" in t.italian)
        self.assertTrue(t.translate() in t.italian)

    def test_dictionary(self):
        d = domain.Dictionary()
        self.assertRaises(ValueError, d.import_from_strings, "Mimmo23", "Lillo2323 &%")
        d.import_from_strings("Alam", "Ciao")
        d.import_from_strings("erim", "Bellissimo")

        self.assertIs(d.size(), 2)
        self.assertTrue(d.exists("Alam"))
        self.assertTrue(d.exists("alam"), "Research should be case-insensitive")
        self.assertFalse(d.exists("Mimmo23"))

        self.assertRaises(ValueError, d.remove, "Mimmo23")
        d.remove("Alam")
        self.assertIs(d.size(), 1)
        self.assertRaises(ValueError, d.remove, "Alam")

        d.add_translation(domain.Translation(alien = "herib", italian = "urub"))
        self.assertIs(d.size(), 2)
        self.assertEqual(d.get_translation("herib"), domain.Translation("herib", "urub"))

    def test_dictionary2(self):
        d = domain.Dictionary.from_translations([domain.Translation(alien = "herib", italian = "urub"), domain.Translation("bil", "Pizza"), domain.Translation("brit", "Vino")])

        self.assertEqual(d.size(), 3)

        d.foreach_trans(lambda t:
                        self.assertTrue(t.alien in d._get_translatable()))

    def test_compex_dict(self):
        d = domain.Dictionary.from_translations(
            [domain.Translation.from_multiple("urub", ["lim", "mim"]),
             domain.Translation.from_multiple("brit", ["rip", "vino"]),
             domain.Translation("tritta", "pippa")])

        self.assertIs(d.single_translations, 1)
        self.assertIs(d.multiple_translations, 2)
        self.assertIs(d.size(), 3)

        d.add_translation(domain.Translation("tritta", "pizza"))
        self.assertIs(d.multiple_translations, 3)
        self.assertIs(d.single_translations, 0)

    def test_multiple_import(self):
        s = "lehti rivista,foglia"
        tk = s.split(" ")

        dic = domain.Dictionary()
        dic.import_from_strings(tk[0].strip(), tk[1].strip())
        self.assertIs(dic.size(), 1)

    def test_wildcard_class(self):
        wild = Wildcard("ter?na")
        self.assertTrue(wild.validate())
        self.assertRaises(ValueError, Wildcard, "ter?na?")
        self.assertTrue(Wildcard("täht?").validate())
        self.assertTrue(Wildcard("?äht").validate())

        self.assertTrue(wild.matches("terina"))
        self.assertTrue(wild.matches("terana"))
        self.assertTrue(wild.matches("teruna"))
        self.assertFalse(wild.matches("terbilna"))
        self.assertFalse(wild.matches("ter8na"))

        wild = Wildcard("tern?")
        self.assertTrue(wild.validate())
        self.assertTrue(wild.matches("terna"))
        self.assertTrue(wild.matches("ternä"))


    def test_wildcard_search(self):
        d = domain.Dictionary.from_translations(
            [domain.Translation.from_multiple("urub", ["lim", "mim"]),
             domain.Translation.from_multiple("urib", ["rip", "vino"]),
             domain.Translation("uretm", "pippa")])

        results: dict[str, domain.Translation] = d.search_wildcard("ur?b")
        self.assertIs(len(results), 2)
        self.assertIsNot(results["urub"], None)
        self.assertIsNot(results["urib"], None)
        self.assertIsNone(results.get("uretm"))

if __name__ == '__main__':
    unittest.main()
