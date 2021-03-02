# coding=utf-8

import codecs
import regex
#import simalign
#from simalign.simalign import *
from nltk.tokenize import word_tokenize
from util import *
import  ast
import os

if __name__ == '__main__':

    uniq_sen = [l.strip('NMT:').strip('English -->').strip() for l in
                 codecs.open(sys.argv[1], 'r', 'utf-8').readlines() if
                 len(l.strip('NMT:').strip('English -->').strip()) > 0]
    uniq_sen = [regex.sub("\\p{C}+", "", regex.sub("\\p{Separator}+", " ", sen)).strip() for sen in  uniq_sen]

    #read all chunk translation in  wx
    chunks = [[l.split('\t')[0].split()[0], l.split('\t')[0].split()[1:], l.split('\t')[1].strip().split()]for l in codecs.open(sys.argv[2], 'r', 'utf-8').readlines()[3:-1]]


    #read root dictionary processed earlier independently
    with open(sys.argv[3], 'r') as f:
        cont = f.readlines()

    dic_root = ast.literal_eval(cont[0])

    # output_best = simalign_batch(best_sen, 'mai')

    #parse and get the chunks from stanford parser



    eng_tok = ' '.join(word_tokenize(uniq_sen[0]))
    f = open('eng-parse.txt', 'w')
    f.write(eng_tok)
    f.close()
    '''
    for l in best_sen[0]:
        f.write(l + '\n')
    f.close()
    '''

    stanford_path = '/home/sriram/alignment/anusaaraka/Parsers/stanford-parser/stanford-parser-4.0.0/'
    os.system( 'java -mx1000m -cp '+ stanford_path + '/*:  edu.stanford.nlp.parser.lexparser.LexicalizedParser -retainTMPSubcategories -outputFormat "xmlTree" '+ stanford_path + '/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz eng-parse.txt 1> eng-parse.xml 2> parse.log')

    f =  open('eng-parse.xml', 'r')
    chunk_sens = xml_parse(f)

    #for ch, ch_hnd in zip(chunk_sens[0], chunks):
    for ch1 in chunk_sens[0]:
        found = 0
        for ch2 in chunks:
            if(ch1[0] == ch2[0]):
                ch1.append(ch2[2])
                found = 1
                break
        if( not found):
            ch1.append(['no_translation'])


    #group smaller chunks inside larger ones.

    group_chunk = {}
    prev_ch_id = []
    for ch in chunk_sens[0]:
        if(ch[0] != 'S1'):
            if set(ch[2]).issubset(set(prev_ch_id)):
                if(ch[0] not in group_chunk):
                    group_chunk[prev_ch_phrase].append([ch[1], ch[2], ch[3]])
            else:
                if('CC' not in ch[0]):
                    group_chunk[ch[0]] = []
                    group_chunk[ch[0]].append([ch[1], ch[2], ch[3]])
                    prev_ch_id = ch[2]
                    prev_ch_phrase = ch[0]


    #align smaller chunk translation to bigger chunk by applying logic
    align_chunk_logic(group_chunk, dic_root)

    eng_chunk_list = []
    hnd_chunk_list = []
    for key in group_chunk:
        ch = group_chunk[key]
        for l in ch[-1]:
            eng_chunk_list.append(l[1])
            hnd_chunk_list.append(l[2])

    eng_full_sen = ' '.join(chunk_sens[0][0][1])
    hnd_full_sen = ' '.join(chunk_sens[0][0][3])

    eng_chunk_list1 = []
    hnd_chunk_list1 = []


    for wd in eng_chunk_list:
        if(type(wd) == list):
            wd1 = list(set(wd))
            if(len(wd1) > 1):
                eng_chunk_list1.append(' '.join(wd))
            else:
                eng_chunk_list1.append(wd1[0])
        else:
            eng_chunk_list1.append(wd)

    for wd in hnd_chunk_list:
        if(type(wd) == list):
            wd1 = list(set(wd))
            if(len(wd1) > 1):
                hnd_chunk_list1.append(' '.join(wd))
            else:
                hnd_chunk_list1.append(wd1[0])
        else:
            hnd_chunk_list1.append(wd)

    print(eng_full_sen)
    print(hnd_full_sen)
    print('\t', '\t'.join(eng_chunk_list1))
    print('\t', '\t'.join(hnd_chunk_list1))



    '''
    filter_chunk_sens = filter_chunk(chunk_sens, chunk_size=5)

    #run simalign
    model = simalign.SentenceAligner()

    eng_str_list = []
    hnd_str_list = []
    eng_str_list_id = []
    hnd_str_list_id = []

    for i in range(1, len(uniq_sen)):
        try:
            hnd_tok = ' '.join(word_tokenize(uniq_sen[i]))
            result = model.get_word_aligns(eng_tok, hnd_tok)
        except:
            print('Error in sen:', eng_tok)
            result = ''

        if not result == '':

            hnd_chunk = get_chunk_align(eng_tok, filter_chunk_sens, hnd_tok, result['itermax'] )
            eng_str_id = ''
            hnd_str_id = ''
            eng_str = ''
            hnd_str = ''

            eng_str_list[i] = []
            hnd_str_list[i] = []
            eng_str_list_id[i] = []
            hnd_str_list_id[i] = []

            for ch, hnd_ch in zip(filter_chunk_sens[0], hnd_chunk):
                eng_str = eng_str + '\t' + (' '.join(ch[1]))
                #eng_str_list[i].append([' '.join(ch[1])])

                hnd_str = hnd_str + '\t' + (' '.join(hnd_ch[0][0]))
                #hnd_str_list[i].append([' '.join(hnd_ch[0][0])])

                eng_str_id = eng_str_id + '\t' + str(ch[2])
                #eng_str_list_id[i].append([str(ch[2])])

                hnd_str_id = hnd_str_id + '\t' + str(hnd_ch[0][1])
                #hnd_str_list_id[i].append([str(hnd_ch[0][1])])

            print('############'+str(i)+'###########', flush=True)
            eng_sen_str = ''
            for j in range(0, len(eng_tok.split())):
                eng_sen_str = eng_sen_str+eng_tok.split()[j]+'_'+str(j)+' '

            hnd_sen_str = ''
            for j in range(0, len(hnd_tok.split())):
                hnd_sen_str = hnd_sen_str+hnd_tok.split()[j]+'_'+str(j)+' '

            print(eng_tok, flush=True)
            print(hnd_tok, flush=True)
            
            print(eng_sen_str, flush=True)
            print(hnd_sen_str, flush=True)
            print(result['itermax'], flush=True)
            
            print(eng_str, flush=True)
            #print(eng_str_id, flush=True)
            print(hnd_str, flush=True)
            #print(hnd_str_id, flush=True)

            #tmp_output.append([sen[i], result['itermax']])

        #output_align_uniq.append([l1_sen, tmp_output])

    eng_str = ''
    hnd_str = ''
    for i in range(0, len(filter_chunk_sens[0])):
        eng_ch = ' '.join(filter_chunk_sens[0][i][1])
        hnd_ch = []
        for j in range (3, len(filter_chunk_sens[0][i])):
            tmp_hnd_str = ' '.join(filter_chunk_sens[0][i][j][0][0])
            hnd_ch.append(tmp_hnd_str)
        hnd_ch1 = list(set(hnd_ch))
        eng_str = eng_str + '\t' + eng_ch
        hnd_str = hnd_str + '\t' + str(hnd_ch1)

    print(eng_tok)
    print(hnd_tok)
    print(eng_str)
    print(hnd_str)

    eng_hnd_chunk = align_eng_hnd_chunk(filter_chunk_sens, output_align_uniq)

    for sen_ch, sen_eng, sen_hnd  in zip(eng_hnd_chunk, best_sen[0], best_sen[1]):
        eng_ch = []
        hnd_ch = []
        for ch in sen_ch:
            eng_ch.append(' '.join(ch[1]))
            tmp_hnd = []
            for hnd in ch[3]:
                tmp_hnd.append(' '.join(hnd[0]))
            hnd_ch.append(list(set(tmp_hnd)))

        hnd_str = ""
        for ch in hnd_ch:
            hnd_str = hnd_str + str(ch)+"\t"

        print(sen_eng)
        print(sen_hnd)
        print('\t'.join(eng_ch))
        print(hnd_str)
        print('----------\n\n')

    '''