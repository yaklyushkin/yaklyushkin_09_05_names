# -*- coding: utf-8 -*-


class Word(object):

    def __init__(self, word, position):
        self.word = word
        self.position = position
        self.next = None
        self.previous = None
        self.chain = None

    def add_to_chain(self, chain):
        self.chain = chain
        if chain.first is None:
            chain.first = self
            chain.last = self
        else:
            self.previous = chain.last
            chain.last.next = self
            chain.last = self

    def remove_from_chain(self):
        if self.previous is not None:
            self.previous.next = self.next
        else:
            self.chain.first = self.next
        if self.next is not None:
            self.next.previous = self.previous
        else:
            self.chain.last = self.previous
        self.chain = None

    def __str__(self):
        if self.previous is not None:
            prev = '"%s" at %d' % (self.previous.word, self.previous.position)
        else:
            prev = None
        if self.next is not None:
            next = '"%s" at %d' % (self.next.word, self.next.position)
        else:
            next = None
        return '"%s" at %d (<%s> <%s>)' % (self.word, self.position, prev, next)

    def __eq__(self, other):
        return (self.word == other.word and self.position == other.position)


class ChainOfWords(object):

    def __init__(self):
        self.first = None
        self.last = None

    def add_word(self, word):
        word.add_to_chain(self)

    def remove_word(self, word):
        word.remove_from_chain()

    def __str__(self):
        result = ''
        for word in self:
            if result != '':
                result += '\n'
            result += str(word)
        return 'chain [\n%s\n]' % result

    def __iter__(self):
        self.current = self.first
        return self

    def __next__(self):
        if self.current is None:
            raise StopIteration
        result = self.current
        self.current = self.current.next
        return result
