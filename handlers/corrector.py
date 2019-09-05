# -*- coding: utf-8 -*-


from handlers.jaro import jaro


class EnteredWords(object):

    def __init__(self):
        self.score = 0
        self.correction = None
        self.words = list()
        self.entered = ''

    def add_word(self, word, index_in_chain):
        self.words.append((index_in_chain, word,))
        if self.entered != '':
            self.entered += ' '
        self.entered += word.word

    def check(self, divided_context_list, probability_limit):
        for candidate in divided_context_list:
            score = jaro(self.entered, candidate)
            if score == 1:
                self.score = 1
                self.correction = candidate
                break
            else:
                if score >= probability_limit and self.score < score:
                    self.score = score
                    self.correction = candidate

    def __str__(self):
        result = ''
        for word in self.words:
            if result != '':
                result += ' '
            result += '%d:"%s"' % (word[0], word[1].word)
        if self.score > 0:
            result += ' (%f "%s")' % (self.score, self.correction)
        return result


class SimilarityChecker(object):

    def __init__(self, divided_context, probability_limit, is_surname_and_name=False):
        self.divided_context = divided_context
        self.probability_limit = probability_limit
        self.is_surname_and_name = is_surname_and_name
        self.entered_list = list()

    def check(self, chain):
        self.entered_list = list()
        for index, word in enumerate(chain):
            entered = EnteredWords()
            entered.add_word(word, index)
            if self.is_surname_and_name:
                if word.next is not None:
                    entered.add_word(word.next, index + 1)
                else:
                    entered = None
            if entered is not None:
                entered.check(self.divided_context, self.probability_limit)
                self.entered_list.append(entered)
