from collections import defaultdict
from itertools import permutations, combinations
import string


class Dictionary:
    def __init__(self, file):
        self.alphabet = list(string.ascii_lowercase)
        self.l = []  # list of all words
        self.d = defaultdict(
            lambda: defaultdict(list)
        )  # dictionary: key 1 = nb of letters key 2 = sorted letters
        with open(file, "r") as f:
            for l in f.readlines():
                wd = l.strip().lower()
                self.d[len(wd)]["".join(sorted(wd))].append(wd)
                self.l.append(wd)
        self.l = sorted(self.l)

    def wordlist(
        self, nb_letters=2, letters=""
    ):  # get list of all words with 'nb_letters' letters and including the letters 'letters'
        l = []
        for key in self.d[nb_letters].keys():
            if all(letter in key for letter in letters):
                l.extend(self.d[nb_letters][key])
        return l

    def anagram(self, wd):  # get all valid words formed by all the letters in 'wd'
        letters = "".join(sorted(wd))
        if letters not in self.d[len(wd)].keys():
            return []
        return self.d[len(wd)][letters]

    def valid(self, wd):  # return bool
        return wd in self.anagram(wd)

    def all_words(
        self, wd
    ):  # return dict nb_letters - list of valid words with nb_letters <= len(wd)
        m = {}
        for i in range(2, len(wd)):
            lst = []
            for j in combinations(wd, i):
                swd = "".join(sorted(j))
                if swd in self.d[i].keys():
                    lst.extend(self.d[i][swd])
            if len(lst) > 0:
                m[i] = lst
        return m

    def words(
        self, wd, nb_letters
    ):  # return list of valid words with nb_letters composed with letters from wd
        m = self.all_words(wd)
        if nb_letters not in m.keys():
            return []
        return m[nb_letters]

    def cousin(self, wd):  # return list of cousins of word wd
        cousins = []
        for i in range(len(wd)):
            for letter in self.alphabet:
                c = wd[:i] + letter + wd[i + 1 :]
                if (c != wd) and self.valid(c):
                    cousins.append(c)
        return cousins

    def suffix(self, wd):  # return list of suffixes
        suffixes = []
        for key in self.d.keys():
            if key > len(wd):
                for k, v in self.d[key].items():
                    if all(letter in k for letter in wd):
                        for word in self.d[key][k]:
                            if word[: len(wd)] == wd:
                                suffixes.append(word)
        return suffixes

    def anagram_plus_one(
        self, wd
    ):  # return dict letter - new word with only one different letter
        m = defaultdict(list)
        anagrams = []
        for letter in self.alphabet:
            wds = self.anagram(wd + letter)
            if len(wds) > 0:
                m[letter].extend(wds)
        return m

    def plus_one_words(self, wd):  # get list of all words possible with one more letter
        all_wds = []
        return sum(self.anagram_plus_one(wd).values(), [])

    def plus_one_letters(
        self, wd
    ):  # which letters lead to a word composed of all letters of wd + this letter
        return sorted(list(self.anagram_plus_one(wd).keys()))

    def plus_one_letter_words(
        self, wd, letter
    ):  # get list of all words possible composed of all letters of wd + the letter as input
        return self.anagram_plus_one(wd)[letter]

    def diff_suppr(
        self, other
    ):  # get all words that were in other and are not available in the current dictionary
        return sorted(list(set(other.l) - set(self.l)))

    def diff_add(
        self, other, nb_letters=0, letters=""
    ):  # get all new words from the other dictionary
        l = []
        if nb_letters > 1:
            l = list(
                set(self.wordlist(nb_letters, letters))
                - set(other.wordlist(nb_letters, letters))
            )
        else:  # 0 means all words
            for key in self.d.keys():
                l.extend(
                    list(
                        set(self.wordlist(key, letters))
                        - set(other.wordlist(key, letters))
                    )
                )
        return sorted(l)