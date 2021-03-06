# coding=utf-8

#import simalign
#from simalign.simalign import *
from util import *




if __name__ == '__main__':

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


