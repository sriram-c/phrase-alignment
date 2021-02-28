# coding=utf-8

import argparse
import regex
import os
import codecs
from simalign.simalign import *
import simalign

import torch.nn.functional as F

from util import *

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="Phrase Alignment of source and target sentence using Heuristics and ML tool",
        epilog="example: python3 align.py path/to/L1/text path/to/L2/text [options]")
    parser.add_argument("uq_path", type=str)
    parser.add_argument("best_path", type=str)
    parser.add_argument("--num-test-sents", type=int, default=None, help="None means all sentences")

    args = parser.parse_args()

    list_uniq_file = os.listdir(args.uq_path)
    list_uniq_file.sort(key=int)
    uniq_sen = [[l.strip('NMT:').strip('English -->').strip() for l in
                 codecs.open(args.uq_path + '/' + f, 'r', 'utf-8').readlines() if
                 len(l.strip('NMT:').strip('English -->').strip()) > 0] for f in list_uniq_file]
    uniq_sen = [[regex.sub("\\p{C}+", "", regex.sub("\\p{Separator}+", " ", sen)).strip() for sen in sen_pair] for
                sen_pair in uniq_sen]


    best_sen = []
    l1_sen = [l.split('\t')[0].strip() for l in codecs.open(args.best_path, 'r', 'utf-8').readlines()]
    l2_sen = [l.split('\t')[1].strip() for l in codecs.open(args.best_path, 'r', 'utf-8').readlines()]
    best_sen.append(l1_sen)
    best_sen.append(l2_sen)

    # output_best = simalign_batch(best_sen, 'mai')

    model = simalign.SentenceAligner()
    output_align_uniq = []
    for sen in uniq_sen:
        l1_sen = sen[0]
        print('processing ', l1_sen)
        tmp_output = []
        for i in range(1, len(sen)):
            result = model.get_word_aligns(l1_sen, sen[i])
            tmp_output.append([sen[i], result['itermax']])
        output_align_uniq.append([l1_sen, tmp_output])

    f = open('eng-parse.txt', 'w')
    for l in best_sen[0]:
        f.write(l + '\n')
    f.close()

    stanford_path = '/home/sriram/anusaaraka/Parsers/stanford-parser/stanford-parser-4.0.0/'
    os.system( 'java -mx1000m -cp '+ stanford_path + '/*:  edu.stanford.nlp.parser.lexparser.LexicalizedParser -retainTMPSubcategories -outputFormat "xmlTree" '+ stanford_path + '/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz eng-parse.txt 1> eng-parse.xml 2> parse.log')

    from util import  *
    f =  open('eng-parse.xml', 'r')
    chunk_sens = xml_parse(f)
    filter_chunk_sens = filter_chunk(chunk_sens, chunk_size=5)


    eng_hnd_chunk = align_eng_hnd_chunk(filter_chunk_sens, output_align_uniq)

    for sen_ch, sen in zip(eng_hnd_chunk, output_align_uniq):
        eng_ch = []
        hnd_ch = []
        for ch in sen_ch:
            eng_ch.append(' '.join(ch[1]))
            tmp_hnd = []
            for hnd in ch[3]:
                tmp_hnd.append(' '.join(hnd[0]))
            hnd_ch.append(tmp_hnd)
        print('\t'.join(eng_ch))
        print('\t'.join(str(hnd_ch)))
        print('----------\n\n-----------')

    print('sri')

