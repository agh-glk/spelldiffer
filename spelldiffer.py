# coding=utf-8
from difflib import SequenceMatcher
from nltk.tokenize import RegexpTokenizer

class StringSpellchecksFinder(object):
    """
    Compares two strings, finding words that been
    """
    def __init__(self, similarity=0.7):
        self.tokenizer = RegexpTokenizer('[\w\'-]+')
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

    def find_best_match(self, sequence_before, sequence_after):
        """
        Finds the best matching of word pairs that are most probable to be mistake+correction pairs
        """
        pairs = []
        possibilities = map(lambda w: map(lambda w2: (w, w2, SequenceMatcher(None, w, w2).ratio()) , sequence_after) , sequence_before)
        for possibility in possibilities:
            possibility = filter(lambda p: p[2] >= self.similarity, possibility)
            if possibility:
                possibility.sort(key=lambda p: p[2], reverse=True)
                pairs.append((possibility[0][0], possibility[0][1]))

        return pairs
