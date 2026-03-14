import unittest
from io import UnsupportedOperation

import src.domain.classes as domain

class TestCase(unittest.TestCase):

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

        self.assertRaises(UnsupportedOperation, d.import_from_strings, "herib", "liliimi")

if __name__ == '__main__':
    unittest.main()
