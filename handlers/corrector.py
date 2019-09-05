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

    def __lt__(self, other):
        if self.score < other.score:
            return True
        elif self.score > other.score:
            return False
        if self.words[0][1].position > other.words[0][1].position:
            return True
        elif self.words[0][1].position < other.words[0][1].position:
            return False
        if self.correction > other.correction:
            return True
        elif self.correction < other.correction:
            return False
        return False

    def __eq__(self, other):
        if not (self.score == other.score):
            return False
        if len(self.words) != len(other.words):
            return False
        for index in range(len(self.words)):
            if self.words[index] != other.words[index]:
                return False
        if not (self.correction == other.correction):
            return False
        return True


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


# Расскомментировать для проверки Исправление 2: упорядочивание по вероятности
"""def read_similarity(chain, check_context, probability_limit, is_surname_and_name):
    if len(check_context) != 0:
        checker = SimilarityChecker(check_context, probability_limit, is_surname_and_name)
        checker.check(chain)
        return checker.entered_list
    else:
        return []
"""


class Corrector(object):

    def __init__(self, check_context, probability_limit, is_surname_and_name):
        self.check_context = check_context
        self.probability_limit = probability_limit
        self.is_surname_and_name = is_surname_and_name

    def read_similarity(self, chain):
        if len(self.check_context) != 0:
            checker = SimilarityChecker(self.check_context, self.probability_limit, self.is_surname_and_name)
            checker.check(chain)
            return checker.entered_list
        else:
            return []

    def prune(self, chain, entered_list):
        result = []
        words_cnt = chain.length
        used_words = [False] * words_cnt
        for entered in entered_list:
            if entered.score == 0:
                continue
            is_used_some_word_already = False
            for word in entered.words:
                if used_words[word[0]]:
                    is_used_some_word_already = True
                    break
            if not is_used_some_word_already:
                for word in entered.words:
                    chain.remove_word(word[1])
                    used_words[word[0]] = True
                if int(entered.score) != 1:
                    result.append(entered)
        return result

    def correct(self, chain):
        entered_list = self.read_similarity(chain)
        entered_list.sort(reverse=True)
        corrections =  self.prune(chain, entered_list)
        return corrections
