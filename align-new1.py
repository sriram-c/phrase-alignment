# coding=utf-8

#import simalign
#from simalign.simalign import *
from util import *
import sys





def noisy_input_hand_corrected():
    return 'cases to be handled'

def noisy_input_automatic_correctd():
    return 'cases to be handled'

def idiomatic_nmt_parser_works():
    return 'cases to be handled'

def idiomatic_nmt_fails_parser_works():
    return 'cases to be handled'

def idiomatic_nmt_works_parser_fails():
    return 'cases to be handled'

def idiomatic_nmt_parser_fails():
    return 'cases to be handled'

def manual_translation():
    return 'cases to be handled'


def anusaaraka_output_quality():
    return 'cases to be handled'


def improving_training_corpus_mutual_bootstrapping():
    return 'cases to be handled'


def different_input_source_sentence():
    return 'cases to be handled'


def default():


    #read uniq sent, chunks-translation
    uniq_sen, chunks, dic_root = read_data()

    #for getting simalign output
    # output_best = simalign_batch(best_sen, 'mai')

    #run stanford parser on English sent
    eng_tok = ' '.join(word_tokenize(uniq_sen[0]))
    stanford_parser(eng_tok)

    #make chunks using constituent parser o/p
    f = open('eng-parse.xml', 'r')
    chunk_sens = xml_parse(f)

    #add hindi translation for each chunk
    add_hindi(chunks, chunk_sens)

    #group smaller chunks into larger chunks
    group_chunk = group_sub_chunks(chunk_sens)

    #align smaller chunk translation to bigger chunk by applying logic
    align_chunk_logic_new(group_chunk, dic_root)


    # for each uniq sen do the aligning process
    for i in range(1, len(uniq_sen)):
        hnd_sen = uniq_sen[i]
        align_hnd_sens(group_chunk, hnd_sen, dic_root, i)

    #print the aligned phrases in tab separated format


    print_align(chunk_sens, group_chunk, uniq_sen)

    return 'processed'


switcher = {

        1: noisy_input_hand_corrected,
        2: noisy_input_automatic_correctd,
        3: idiomatic_nmt_parser_works,
        4: idiomatic_nmt_fails_parser_works,
        5: idiomatic_nmt_works_parser_fails,
        6: idiomatic_nmt_parser_fails,
        7: manual_translation,
        8: anusaaraka_output_quality,
        9: improving_training_corpus_mutual_bootstrapping,
        10: different_input_source_sentence,
        11: default

    }



def select_case(argument):
    func = switcher.get(argument, 'nothing')
    return func()



if __name__ == '__main__':

    case = int(sys.argv[3])

    result = select_case(case)
    print(result)

