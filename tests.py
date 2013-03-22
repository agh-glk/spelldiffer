# coding=utf-8
from unittest import TestCase
from spelldiffer import StringSpellchecksFinder


class TestStringSpellchecksFinder(TestCase):
    def setUp(self):
        self.sf = StringSpellchecksFinder()

    def test_find_best_match(self):
        self.assertEqual(self.sf.find_best_match([u'this', u'is', u'it', u'blach'], [u'thiss', u'blah', u'dlah']),
                         [(u'this', u'thiss'), (u'blach', u'blah')])


    def test_find(self):
        self.assertEqual(self.sf.find(
            u"Polak znowu uzyskal prawie njlepszy czas 14.39,6 minuty. Nasz kierowca ponownie okazał się lepszy tlyko od Jana Kopecky'ego.",
            u"Polak znowu uzyskał njlepsy najlepszy czas 14.39,6 minuty. nasz byly kierowca ponownie się lepszy tylko od Jana Kopecky'ego."

        ),
                         [(u'uzyskal', u'uzyskał'),
                          (u'njlepszy', u'najlepszy'),
                          (u'tlyko', u'tylko')]
        )
