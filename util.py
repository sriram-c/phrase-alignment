# coding=utf-8

import sys
import re
from bs4 import BeautifulSoup, Tag, NavigableString
import string
import codecs
import regex
import ast
from nltk.tokenize import word_tokenize
import os


def print_align(chunk_sens, group_chunk, uniq_sen):

    eng_chunk_list = []
    hnd_chunk_list = []
    for key in group_chunk:
        ch = group_chunk[key]
        for l in ch[-1]:
            eng_chunk_list.append(l[1])
            hnd_chunk_list.append(l[2])

    eng_full_sen = uniq_sen[0]
    hnd_full_sen = uniq_sen[1]

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


def read_data():


    uniq_sen = [l.strip('NMT:').strip('English -->').strip() for l in
                 codecs.open(sys.argv[1], 'r', 'utf-8').readlines() if
                 len(l.strip('NMT:').strip('English -->').strip()) > 0]
    uniq_sen = [regex.sub("\\p{C}+", "", regex.sub("\\p{Separator}+", " ", sen)).strip() for sen in  uniq_sen]

    #read all chunk translation in  wx
    #chunks = [[l.split('\t')[0].split()[0], l.split('\t')[0].split()[1:], l.split('\t')[1].strip().split()]for l in codecs.open(sys.argv[2], 'r', 'utf-8').readlines()[1:-1]]
    chunks = [[l.split('\t')[0].split()[0], l.split('\t')[1].split(), l.split('\t')[2].split()]for l in codecs.open(sys.argv[2], 'r', 'utf-8').readlines()[1:]]


    #read root dictionary processed earlier independently
    with open(sys.argv[3], 'r') as f:
        cont = f.readlines()

    dic_root = ast.literal_eval(cont[0])

    return uniq_sen, chunks, dic_root


def stanford_parser(eng_tok):

    #parse and get the chunks from stanford parser
    #eng_tok = ' '.join(word_tokenize(uniq_sen[0]))
    f = open('eng-parse.txt', 'w')
    f.write(eng_tok)
    f.close()

    stanford_path = '/home/sriram/alignment/anusaaraka/Parsers/stanford-parser/stanford-parser-4.0.0/'
    #stanford_path = '/home/sriram/anusaaraka/Parsers/stanford-parser/stanford-parser-4.0.0/'
    os.system( 'java -mx1000m -cp '+ stanford_path + '/*:  edu.stanford.nlp.parser.lexparser.LexicalizedParser -retainTMPSubcategories -outputFormat "xmlTree" '+ stanford_path + '/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz eng-parse.txt 1> eng-parse.xml 2> parse.log')

def print_chunks(chunk_sens):

    #print the groups to the file to be translated by NMT.
    for ch in chunk_sens[0]:
        print(ch[0]+ '\t' + ' '.join(ch[1]))

def add_hindi(chunks, chunk_sens):
    #keep hindi translated sentences into chunk_sens
    #for ch, ch_hnd in zip(chunk_sens[0], chunks):
    for ch1 in chunk_sens[0]:
        found = 0
        for ch2 in chunks:
            if(ch1[0] == ch2[0]):
                ch1.append(ch2[2])
                found = 1
                break
        if( not found):
            ch1.append(['@no_translation'])


def group_sub_chunks(chunk_sens):

    #group smaller chunks inside larger ones.

    group_chunk = {}
    prev_ch_id = []
    for ch in chunk_sens[0]:
        if(ch[0] != 'S1'):
            if prev_ch_id != [] and set(ch[2]).issubset(set(prev_ch_id)):
                    if(ch[0] not in group_chunk):
                        group_chunk[prev_ch_phrase].append([ch[0], ch[1], ch[2], ch[3]])
            else:
                # if('CC' not in ch[0]):
                group_chunk[ch[0]] = []
                group_chunk[ch[0]].append([ch[0], ch[1], ch[2], ch[3]])
                prev_ch_id = ch[2]
                prev_ch_phrase = ch[0]

    return group_chunk


def print_groups(chunk_sens):
    # print the groups to the file to be translated by NMT.
    for ch in chunk_sens[0]:
        print(ch[0]+ '\t' + ' '.join(ch[1]))


def find_leaf(tag, phrase, flag):
    tmp_wd = []
    tmp_id = []
    tmp_wid = []

    if (flag):
        for wd in tag.find_all('leaf'):
            tmp_wd.append(wd['value'])
            #tmp_wid.append(str(wd['id']))
            tmp_wid.append((wd['id']))
        phrase.append([tag['value'] + str(tag['id']), tmp_wd, tmp_wid])

    elif (tag['value'] == 'CC'):
        cc_wd = tag.find_all('leaf')[0]['value']
        cc_wd_id = tag.find_all('leaf')[0]['id']

    elif (re.match(
            r'^NP|NP-TMP|WHNP|NNP|PP|WHPP|ADJP|WHADJP|WHADVP|ADVP|WHAVP|X|NAC|NML|CONJP|FRAG|INTJ|LST|NAC|NX|PRC|PRN|PRT|RRC|UCP|ROOT|,$',
            tag['value']) and (tag.name != 'leaf')):
        for wd in tag.find_all('leaf'):
            tmp_wd.append(wd['value'])
            #tmp_wid.append(str(wd['id']))
            tmp_wid.append((wd['id']))
        phrase.append([tag['value'] + str(tag['id']), tmp_wd, tmp_wid])


def find_lwg(tag, tmp_lwg, tmp_lwg_id, flag, phrase):
    for tag1 in tag.contents:
        if (isinstance(tag1, Tag)):
            if (re.match(r'^VB|ADVP|ADJP|RB|PRT|TO|MD', tag1['value'])):
                # tmp_val = tag1.find_all('leaf')[0]['value']
                tmp_id = tag1.find_all('leaf')[0]['id']
                for n in tag1.find_all('leaf'):
                    tmp_lwg.append(n['value'])
                    tmp_lwg_id.append(n['id'])

                # tmp_lwg.append(tmp_val + '_' + str(tmp_id))
                #tmp_lwg_id.append(str(tmp_id))
                # tmp_lwg_id.append((tmp_id))

            elif (re.match(r'^VP|ADJP', tag1['value'])):
                find_lwg(tag1, tmp_lwg, tmp_lwg_id, 1, phrase)
    if (flag == 0):
        phrase.append([tag['value'] + str(tag['id']) + '_LWG', tmp_lwg, tmp_lwg_id])


def process_tag(tag, phrase):
    if (isinstance(tag, Tag)):
        if (tag['value'] == 'VP') and (tag.parent['value'] != 'VP'):
            tmp_lwg = []
            tmp_lwg_id = []
            find_lwg(tag, tmp_lwg, tmp_lwg_id, 0, phrase)
            for tag1 in tag.contents:
                if (isinstance(tag1, Tag)):
                    process_tag(tag1, phrase)


        elif (re.match(r'CC', tag['value'])):
            find_leaf(tag, phrase, 0)

        else:
            find_leaf(tag, phrase, 0)
            for tag1 in tag.contents:
                if (isinstance(tag1, Tag)):
                    process_tag(tag1, phrase)

def xml_parse(fp):

    soup = BeautifulSoup("<node>" + ''.join(fp.readlines()) + "</node>", 'lxml-xml')
    all_root = soup.find_all(value='ROOT')

    all_chunk = []
    for root in all_root:
        id = 1
        for node in root.find_all('leaf'):
            node['id'] = id
            id += 1

        id = 1
        for node in root.find_all('node'):
            node['id'] = id
            id += 1

        phrase = []
        for ch in root.contents:
            if (isinstance(ch, Tag)):
                process_tag(ch, phrase)

        all_chunk.append(phrase)
    return  all_chunk



def align_chunk_logic_new(group_chunk, dic_root):

    #find different surface forms by comparing root
    for key in group_chunk:
        ch = group_chunk[key]
        long_chunk_hnd = ch[0][3]
        long_chunk_hnd_root = [dic_root[l] if l in dic_root else l for l in long_chunk_hnd]
        long_chunk_wd_alt = {}

        #find alternative of each word
        for wd, wd_rt in zip(long_chunk_hnd, long_chunk_hnd_root):
            long_chunk_wd_alt[wd] = [wd]
            for i in range(1, len(ch)):
                tmp_root = [dic_root[l] if l in dic_root else l for l in ch[i][3]]
                if wd not in ch[i][3] and  wd_rt in tmp_root:
                    indx = tmp_root.index(wd_rt)
                    wd_alt = ch[i][3][indx]
                    if wd_alt not in long_chunk_wd_alt[wd]:
                        long_chunk_wd_alt[wd].append(wd_alt)

        ch.append(long_chunk_wd_alt)

    #start aligning each larger chunk
    for key in group_chunk:
        align_wds = {}
        align_eng_wds = []  # listof eng wds aligned
        align_hnd_wds = []  # list of hnd wds aligned
        ch = group_chunk[key]
        dic_wd_alt = ch[-1]
        align_wd_ids = []

        # process each smaller chunk in large chunk
        for i in range(len(ch) - 2, -1, -1):
            tmp_phrase_name = ch[i][0]
            tmp_hnd = ch[i][3]
            tmp_eng = ch[i][1]
            tmp_eng_wd_id = ch[i][2]

            #check if prev phrase is pp and there is only 1 prepostion
            #then consider the PP phrase as NP and add it instead of this NP.
            flag = 0
            for id in tmp_eng_wd_id:
                if id in align_wd_ids:
                    flag = 1
            if (not flag):
                if(i != 0):
                    prev_phrase_name = ch[i - 1][0]
                    prev_eng_wd_id = ch[i - 1][2]
                    prev_hnd = ch[i - 1][3]

                    if(re.match(r'^NP', tmp_phrase_name)) and (re.match(r'^PP', prev_phrase_name)) and (len(prev_eng_wd_id) - len(tmp_eng_wd_id) == 1):
                        tmp_key_id = '_'.join(str(id) for id in prev_eng_wd_id)
                        align_wds[tmp_key_id] = prev_hnd
                        for id in prev_eng_wd_id:
                            align_wd_ids.append(id)
                    elif (re.match(r'^NP|^VP', tmp_phrase_name)):
                        tmp_key_id = '_'.join(str(id) for id in tmp_eng_wd_id)
                        align_wds[tmp_key_id] = tmp_hnd
                        for id in tmp_eng_wd_id:
                            align_wd_ids.append(id)
                    #for VP and ADJP join these two and put the ids in the list
                    # elif(re.match(r'^ADJPP', tmp_phrase_name)):

                else:
                    tmp_key_id = '_'.join(str(id) for id in tmp_eng_wd_id)
                    align_wds[tmp_key_id] = tmp_hnd
                    for id in tmp_eng_wd_id:
                        align_wd_ids.append(id)


        ch.append(align_wd_ids)
        # change ids to string (e.g 15 to '15') for
        # further storing multiple ids '1_2_3'
        align_wds1 = {}
        for key5 in align_wds:
            align_wds1[str(key5)] = align_wds[key5]
        ch.append(align_wds1)

    # Create a list eng hnd list in sequence for storing the final alignment
    for key11 in group_chunk:
        ch = group_chunk[key11]
        eng_long_chunk = ch[0][1]
        start_id = ch[0][2][0]
        end_id = ch[0][2][-1]
        align_wds = ch[-1]
        align_wd_ids = ch[-2]
        found_eng_wd = []
        align_eng_hnd_list = []

        # start from the first word to last word
        for i in range(start_id, end_id + 1):
            if i in align_wd_ids:
                if str(i) in align_wds:
                    if (i - start_id < len(eng_long_chunk)):  # temporary fix for sent e.g 0007 'tackled solved'
                        tmp_eng = eng_long_chunk[i - start_id]
                        tmp_hnd = align_wds[str(i)]
                        if(i not in found_eng_wd):
                            found_eng_wd.append(i)
                        chunk_name = align_wds[str(i)]
                        align_eng_hnd_list.append([str(i), tmp_eng, tmp_hnd])
                        # align_wds[str(i)].append(tmp_eng)

                else:  # for multiple id cases (e.g. 1_2_3 ) search the align_wds dic
                    for key12 in align_wds:
                        tmp_ids = key12.split('_')
                        if (len(tmp_ids)) > 1:
                            if str(i) in tmp_ids and i not in found_eng_wd:
                                tmp_eng_list = []
                                tmp_hnd = align_wds[key12]
                                for id in tmp_ids:
                                    if (int(id) - start_id < len( eng_long_chunk)):  # temporary fix for sent e.g 0007 'tackled solved'
                                        tmp_eng_list.append(eng_long_chunk[int(id) - start_id])
                                        if (id not in found_eng_wd):
                                            found_eng_wd.append(int(id))

                                align_eng_hnd_list.append([key12, tmp_eng_list, tmp_hnd])
                                # align_wds[key12].append(tmp_eng_list)
                                break


            else:  # if no alignment , then keep it empty
                if (i - start_id < len(eng_long_chunk)) and i not in found_eng_wd:  # temporary fix for sent e.g 0007 'tackled solved'
                    tmp_eng = eng_long_chunk[i - start_id]
                    align_eng_hnd_list.append([i, tmp_eng, ['']])
        ch.append(align_eng_hnd_list)




def align_direct_n_root_matching(group_chunk, hnd_sen, hnd_sen_root, root, count):

    #align each chunk in group_chnk
    for key in group_chunk:
        ch = group_chunk[key]
        for grp in ch[-1]:
            id = grp[0]
            eng_ch = grp[1]
            hnd_ch = grp[2]
            hnd_ch_root = [root[l] if l in root else l for l in hnd_ch]

            wds_match = []
            wds_match_id = []

            #if direct matching is there nothing to do
            if(' '.join(hnd_ch) not in hnd_sen):
                #search the beginnning word
                for i in range(0, len(hnd_ch)):
                    tmp_wd = hnd_ch[i]
                    if hnd_ch[i] in hnd_sen.split():
                        wds_match.append(hnd_ch[i])
                        wds_match_id.append(hnd_sen.split().index(hnd_ch[i]) + 1)

                    #match the root also
                    elif hnd_ch_root[i] in hnd_sen_root:
                        indx = hnd_sen_root.index(hnd_ch_root[i])
                        wds_match.append(hnd_sen.split()[indx])
                        wds_match_id.append(indx+1)

            #if match not present then add it
            if(count == 1 ): # for the 1st sentence create grp[3]
                grp.append([[wds_match]])
            else:
                if [wds_match] not in grp[3]:
                    grp[3].append([wds_match])


# def align_missing_id(group_chunk, hnd_sen, hnd_sen_root, root):


def align_hnd_sens(group_chunk, hnd_sen, root, count):

    hnd_sen_root = [root[l] if l in root else l for l in hnd_sen.split()]
    align_direct_n_root_matching(group_chunk, hnd_sen, hnd_sen_root, root, count)
    print('sri')



def simalign_batch(original_corpora, matching_methods):
    convert_to_words = False
    device = torch.device("cpu")

    # --------------------------------------------------------
    embed_loader = EmbeddingLoader(model="bert-base-multilingual-cased", device=device)

    words_tokens = []
    for sent_id in range(len(original_corpora[0])):
        l1_tokens = [embed_loader.tokenizer.tokenize(word) for word in original_corpora[0][sent_id].split()]
        l2_tokens = [embed_loader.tokenizer.tokenize(word) for word in original_corpora[1][sent_id].split()]
        words_tokens.append([l1_tokens, l2_tokens])

    sentences_bpe_lists = []
    sentences_b2w_map = []
    for sent_id in range(len(words_tokens)):
        sent_pair = [[bpe for w in sent for bpe in w] for sent in words_tokens[sent_id]]
        b2w_map_pair = [[i for i, w in enumerate(sent) for bpe in w] for sent in words_tokens[sent_id]]
        sentences_bpe_lists.append(sent_pair)
        sentences_b2w_map.append(b2w_map_pair)

    corpora_lengths = [len(corpus) for corpus in original_corpora]
    if min(corpora_lengths) != max(corpora_lengths):
        LOG.warning("Mismatch in corpus lengths: " + str(corpora_lengths))
        raise ValueError('Cannot load parallel corpus.')

    # --------------------------------------------------------
    all_matching_methods = {"a": "inter", "m": "mwmf", "i": "itermax", "f": "fwd", "r": "rev"}
    matching_methods = [all_matching_methods[m] for m in matching_methods]

    ds = [(idx, original_corpora[0][idx], original_corpora[1][idx]) for idx in range(len(original_corpora[0]))]
    data_loader = torch.utils.data.DataLoader(ds, batch_size=100, shuffle=False)

    output = {}
    for ext in matching_methods:
        output[ext] = []

    for batch_id, batch_sentences in enumerate(data_loader):
        batch_vectors_src = embed_loader.get_embed_list(batch_sentences[1])
        batch_vectors_trg = embed_loader.get_embed_list(batch_sentences[2])
        btach_sim = None
        if not convert_to_words:
            batch_vectors_src = F.normalize(batch_vectors_src, dim=2)
            batch_vectors_trg = F.normalize(batch_vectors_trg, dim=2)

            btach_sim = torch.bmm(batch_vectors_src, torch.transpose(batch_vectors_trg, 1, 2))
            btach_sim = ((btach_sim + 1.0) / 2.0).cpu().detach().numpy()

        batch_vectors_src = batch_vectors_src.cpu().detach().numpy()
        batch_vectors_trg = batch_vectors_trg.cpu().detach().numpy()

        for in_batch_id, sent_id in enumerate(batch_sentences[0].numpy()):
            sent_pair = sentences_bpe_lists[sent_id]
            vectors = [batch_vectors_src[in_batch_id, :len(sent_pair[0])],
                       batch_vectors_trg[in_batch_id, :len(sent_pair[1])]]

            if not convert_to_words:
                sim = btach_sim[in_batch_id, :len(sent_pair[0]), :len(sent_pair[1])]
            else:
                vectors = SentenceAligner.average_embeds_over_words(vectors, words_tokens[sent_id])
                sim = SentenceAligner.get_similarity(vectors[0], vectors[1])

            all_mats = {}

            sim = SentenceAligner.apply_distortion(sim, 0.0)

            all_mats["fwd"], all_mats["rev"] = SentenceAligner.get_alignment_matrix(sim)
            all_mats["inter"] = all_mats["fwd"] * all_mats["rev"]
            if "mwmf" in matching_methods:
                all_mats["mwmf"] = SentenceAligner.get_max_weight_match(sim)
            if "itermax" in matching_methods:
                all_mats["itermax"] = SentenceAligner.iter_max(sim)

            raw_aligns = {x: [] for x in matching_methods}
            b2w_aligns = {x: set() for x in matching_methods}
            log_aligns = []

            for i in range(len(vectors[0])):
                for j in range(len(vectors[1])):
                    for ext in matching_methods:
                        if all_mats[ext][i, j] > 0:
                            raw_aligns[ext].append('{}-{}'.format(i, j))
                            b2w_aligns[ext].add(
                                '{}-{}'.format(sentences_b2w_map[sent_id][0][i], sentences_b2w_map[sent_id][1][j]))
                            if ext == "inter":
                                log_aligns.append('{}-{}:({}, {})'.format(i, j, sent_pair[0][i], sent_pair[1][j]))

            for ext in matching_methods:
                output[ext].append(' '.join(sorted(b2w_aligns[ext])))

    return output
