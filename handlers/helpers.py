# -*- coding: utf-8 -*-


from handlers.words import Word, ChainOfWords


def parse_chains_of_words(text):
    result = []
    position = 0
    current_chain = None
    for word in text.split(' '):
        if word[0].isupper():
            if word != 'I':
                if current_chain is None:
                    current_chain = ChainOfWords()
                w = Word(word, position)
                current_chain.add_word(w)
            else:
                if current_chain is not None:
                    result.append(current_chain)
                    current_chain = None
        else:
            if current_chain is not None:
                result.append(current_chain)
                current_chain = None
        position += len(word) + 1
    if current_chain is not None:
        result.append(current_chain)
    return result


def split_context_by_length(context):
    result = {'2': list(), '1': list()}
    for word in context:
        if word.find(' ') != -1:
            result['2'].append(word)
        else:
            result['1'].append(word)
    return result
