# -*- coding: utf-8 -*-


import json

from handlers.corrector import Corrector
from handlers.helpers import parse_chains_of_words, reverse_name_and_surname, split_context_by_length


def read_context(file_path):
    with open(file_path, 'r', encoding='utf8') as infile:
        data = json.load(infile)
    return data


def read_texts(file_path):
    with open(file_path, 'r', encoding='utf8') as infile:
        data = [line.strip() for line in infile.readlines() if line.strip() != '']
    return data


def prepare(full_context, probability_limit, text_list):
    divided_context = split_context_by_length(full_context)
    context_correctors = list()
    check_context = divided_context.get('2', [])
    if len(check_context) != 0:
        corrector = Corrector(check_context, probability_limit, True)
        context_correctors.append(('surname and name', corrector,))
        reversed_context = reverse_name_and_surname(check_context)
    else:
        reversed_context = None
    check_context = divided_context.get('1', [])
    if len(check_context) != 0:
        corrector = Corrector(check_context, probability_limit, False)
        context_correctors.append(('only name', corrector,))
    if reversed_context is not None:
        corrector = Corrector(reversed_context, probability_limit, False)
        context_correctors.append(('reversed surname and name', corrector,))

    chains_list = list()
    for text in text_list:
        chains_list.append(parse_chains_of_words(text))
    
    return chains_list, context_correctors


def find_corrections(chain, context_correctors):
    result = {}
    for corrector in context_correctors:
        corrections = corrector[1].correct(chain)
        if len(corrections) != 0:
            result[corrector[0]] = corrections
    return result


def read_corrections_list(chains_list, context_correctors):
    corrections = list()
    for chains in chains_list:
        tmp_result = list()
        for chain in chains:
            founded = find_corrections(chain, context_correctors)
            for key in founded.keys():
                for word in founded[key]:
                    dummy = (word.words[0][1].position, word.entered, word.correction, word.score, key,)
                    tmp_result.append(dummy)
        corrections.append(tmp_result)
    return corrections


def save_corrections_to_json(corrections, file_path):    
    with open(file_path, 'w', encoding='utf8') as outfile:
        json.dump(corrections, outfile)
