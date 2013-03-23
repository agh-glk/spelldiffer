# coding=utf-8

# © 2013 Krzysztof Dorosz AGH GLK
# License: free for scientific use


import argparse
from difflib import SequenceMatcher
from xml.etree.cElementTree import iterparse
from nltk.tokenize import RegexpTokenizer
import sys


class SpellchecksFinder(object):
    def find_best_match(self, sequence_before, sequence_after):
        """
        Finds the best matching of elements pairs that are most probable pairs
        """
        pairs = []
        possibilities = map(lambda element1: map(lambda element2: (element1, element2, SequenceMatcher(None, element1, element2).ratio()) , sequence_after) , sequence_before)
        for possibility in possibilities:
            possibility = filter(lambda p: p[2] >= self.similarity, possibility)
            if possibility:
                possibility.sort(key=lambda p: p[2], reverse=True)
                pairs.append((possibility[0][0], possibility[0][1]))
        return pairs

class StringSpellchecksFinder(SpellchecksFinder):
    """
    Compares two strings, finding words that been
    """
    def __init__(self, similarity=0.7):
        self.tokenizer = RegexpTokenizer('[\w-]+')
        self.similarity = similarity

    def find(self, text_before, text_after):
        """
        Finds all spellchecks tuple(mistake, correction) in the given text
        """
        spellchecks = []
        text_before_tokens = map(lambda x: x.lower(), self.tokenizer.tokenize(text_before))
        text_after_tokens = map(lambda x: x.lower(), self.tokenizer.tokenize(text_after))
        diff_matching = SequenceMatcher(None, text_before_tokens, text_after_tokens)
        for difference in filter(lambda x: x[0] == 'replace', diff_matching.get_opcodes()):
            sequence_before = text_before_tokens[difference[1]:difference[2]]
            sequence_after = text_after_tokens[difference[3]:difference[4]]
            spellchecks += self.find_best_match(sequence_before, sequence_after)
        return spellchecks

class TextSpellchecksFinder(SpellchecksFinder):
    def __init__(self, similarity=0.7):
        self.string_finder = StringSpellchecksFinder(similarity=similarity)
        self.similarity = similarity

    def find(self, text_before, text_after):
        spellchecks = []
        text_before_lines = text_before.splitlines()
        text_after_lines = text_after.splitlines()
        diff_matching = SequenceMatcher(lambda x: bool(x.strip()), text_before_lines, text_after_lines)
        for difference in filter(lambda x: x[0] == 'replace', diff_matching.get_opcodes()):
            sequence_before = text_before_lines[difference[1]:difference[2]]
            sequence_after = text_after_lines[difference[3]:difference[4]]
            line_pairs = self.find_best_match(sequence_before, sequence_after)
            for line1, line2 in line_pairs:
                spellchecks += self.string_finder.find(line1, line2)
        return spellchecks

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Reads two files and generates list of "mistake, correction" pairs.')
    parser.add_argument('--before', type=argparse.FileType('r'), metavar='FILE', help="UTF-8 text file before changes")
    parser.add_argument('--after', type=argparse.FileType('r'), metavar='FILE', help="UTF-8 text file after changes")
    parser.add_argument('--wiki', type=argparse.FileType('r'), metavar='FILE', help="Wikipedia XML file")
    options = parser.parse_args()
    finder = TextSpellchecksFinder()
    if options.wiki:

        last = None
        last_title = None
        for action, elem in iterparse(options.wiki):

            if elem.tag.endswith('}title'):
                last_title = elem.text
                print "##", last_title


            if elem.tag.endswith('}page'):
                    last = None

            if elem.tag.endswith('}text'):
                if last is None:
                    last = elem
                else:
                    print "+",
                    if last.text and elem.text:
                        corrections = finder.find(last.text, elem.text)
                        if corrections:
                            print "#", last_title
                            print "\n".join(map(lambda (w,c): u'%s, %s' % (w, c), corrections))


    else:

        corrections = finder.find(options.before.read().decode('utf-8'), options.after.read().decode('utf-8'))
        print "\n".join(map(lambda (w,c): u'%s, %s' % (w, c), corrections))
