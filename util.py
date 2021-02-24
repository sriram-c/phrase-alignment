import sys
import re
from bs4 import BeautifulSoup, Tag, NavigableString
import string


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

        '''

        if (len(list(tag.previous_siblings)) > 1):
            prev_sib = list(tag.previous_siblings)[1]
            prev_sib1 = prev_sib['value'] + str(prev_sib['id'])
        else:
            prev_sib1 = 'NOT FOUND'

        if (len(list(tag.next_siblings)) > 1):
            next_sib = list(tag.next_siblings)[1]
            next_sib1 = next_sib['value'] + str(next_sib['id'])
        else:
            next_sib1 = 'NOT FOUND'
        '''

        #phrase.append([tag['value'] + str(tag['id']), prev_sib1, next_sib1, cc_wd])
        phrase.append([tag['value'] + str(tag['id']), [cc_wd], [cc_wd_id]])

        '''
        if (prev_sib1 != 'NOT FOUND'):
            find_leaf(prev_sib, phrase, 1)
        if (next_sib1 != 'NOT FOUND'):
            find_leaf(next_sib, phrase, 1)
        '''

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
            if (re.match(r'^VB|ADVP|RB|PRT|TO|MD', tag1['value'])):
                tmp_val = tag1.find_all('leaf')[0]['value']
                tmp_id = tag1.find_all('leaf')[0]['id']
                tmp_lwg.append(tmp_val + '_' + str(tmp_id))
                #tmp_lwg_id.append(str(tmp_id))
                tmp_lwg_id.append((tmp_id))

            elif (re.match(r'^VP', tag1['value'])):
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


def filter_chunk(all_chunk, chunk_size):

    all_filter_chunk = all_chunk.copy()
    for i in range(0,len(all_chunk)):
        store_ids = []
        all_filter_chunk[i] = []
        for j in range(0, len(all_chunk[i])):
            if not re.match(r'S', all_chunk[i][j][0]):
                ids = all_chunk[i][j][2]
                tmp_str = ' '.join(all_chunk[i][j][1])
                exclude = set(string.punctuation)
                s = ''.join(ch for ch in tmp_str if ch not in exclude)
                if (not set(ids).issubset(set(store_ids))) and len(s.split()) < chunk_size:
                    all_filter_chunk[i].append(all_chunk[i][j])
                    store_ids.extend(ids)
    return all_filter_chunk


def get_chunk_align(eng_sen, eng_sen_chunk, hnd_sen, align_result):
    align_eng_hnd = []
    for ch in eng_sen_chunk[0]:
        if not (re.match('CC', ch[0])):
            chunk_id = ch[2]
            hnd_id = []
            tmp_hid = []
            tmp_hid_wd = []
            for ids in chunk_id:
                for aid in align_result:
                    if aid[0] == int(ids):
                        tmp_hid.append(aid[1])
            tmp_hid1 = list(set(tmp_hid))
            tmp_hid1.sort()
            for tid in tmp_hid1:
                tmp_hid_wd.append(hnd_sen.split()[tid])
            hnd_id.append([tmp_hid_wd, tmp_hid1])
        align_eng_hnd.append(hnd_id)
        ch.append(hnd_id)

    return align_eng_hnd

def align_eng_hnd_chunk(filter_chunk_sens, output_align_uniq):
    eng_hnd_chunk = filter_chunk_sens.copy()
    for sen, align_sen in zip(eng_hnd_chunk, output_align_uniq):
        for ch in sen:
            if not (re.match('CC', ch[0])):
                chunk_id = ch[2]
                hnd_id = []
                for aligns in align_sen[1]:
                    tmp_hid = []
                    tmp_hid_wd = []
                    for ids in chunk_id:
                        for aid in aligns[1]:
                            if aid[0] == int(ids):
                                tmp_hid.append(aid[1])
                    tmp_hid1 = list(set(tmp_hid))
                    for tid in tmp_hid1:
                        tmp_hid_wd.append(aligns[0].split()[tid])
                    hnd_id.append([tmp_hid_wd, tmp_hid1])
                ch.append(hnd_id)

    return eng_hnd_chunk



def align_chunk_logic_new(group_chunk, dic_root):

    #find different surface forms by comparing root
    for key in group_chunk:
        ch = group_chunk[key]
        long_chunk_hnd = ch[0][2]
        long_chunk_hnd_root = [dic_root[l] if l in dic_root else l for l in long_chunk_hnd]
        long_chunk_wd_alt = {}

        #find alternative of each word
        for wd, wd_rt in zip(long_chunk_hnd, long_chunk_hnd_root):
            long_chunk_wd_alt[wd] = [wd]
            for i in range(1, len(ch)):
                tmp_root = [dic_root[l] if l in dic_root else l for l in ch[i][2]]
                if wd not in ch[i][2] and  wd_rt in tmp_root:
                    indx = tmp_root.index(wd_rt)
                    wd_alt = ch[i][2][indx]
                    if wd_alt not in long_chunk_wd_alt[wd]:
                        long_chunk_wd_alt[wd].append(wd_alt)

        ch.append(long_chunk_wd_alt)

    for key in group_chunk:
        align_wds = {}
        align_eng_wds = []  # listof eng wds aligned
        align_hnd_wds = []  # list of hnd wds aligned
        ch = group_chunk[key]
        dic_wd_alt = ch[-1]
        align_wd_ids = []
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

                else:
                    if(re.match(r'^NP|^VP', tmp_phrase_name)):
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
        align_wds = ch[-2]
        align_wds_ids = ch[-1]
        found_eng_wd = []
        align_eng_hnd_list = []

        # start from the first word to last word
        for i in range(start_id, end_id + 1):
            if i in align_wds_ids:
                if str(i) in align_wds:
                    if (i - start_id < len(eng_long_chunk)):  # temporary fix for sent e.g 0007 'tackled solved'
                        tmp_eng = eng_long_chunk[i - start_id]
                        tmp_hnd = align_wds[str(i)]
                        found_eng_wd.append(i)
                        chunk_name = align_wds[str(i)]
                        align_eng_hnd_list.append([str(i), tmp_eng, tmp_hnd])
                        # align_wds[str(i)].append(tmp_eng)

                else:  # for multiple id cases (e.g. 1_2_3 ) search the align_wds dic
                    for key12 in align_wds:
                        tmp_ids = key12.split('_')
                        if (len(tmp_ids)) > 1:
                            if str(i) in tmp_ids:
                                tmp_eng_list = []
                                tmp_hnd = align_wds[key12]
                                for id in tmp_ids:
                                    if (int(id) - start_id < len(
                                            eng_long_chunk)):  # temporary fix for sent e.g 0007 'tackled solved'
                                        tmp_eng_list.append(eng_long_chunk[int(id) - start_id])
                                        found_eng_wd.append(int(id))

                                align_eng_hnd_list.append([key12, tmp_eng_list, tmp_hnd])
                                # align_wds[key12].append(tmp_eng_list)
                                break


            else:  # if no alignment , then keep it empty
                if (i - start_id < len(eng_long_chunk)):  # temporary fix for sent e.g 0007 'tackled solved'
                    tmp_eng = eng_long_chunk[i - start_id]
                    align_eng_hnd_list.append([i, tmp_eng, ['empty']])
        ch.append(align_eng_hnd_list)

    print('sriram')
    print('sriram1')


def align_chunk_logic(group_chunk, dic_root):

    #align smaller chunks inside long chunk by applying various logic

    #find different surface forms by comparing root
    for key in group_chunk:
        ch = group_chunk[key]
        long_chunk_hnd = ch[0][2]
        long_chunk_hnd_root = [dic_root[l] if l in dic_root else l for l in long_chunk_hnd]
        long_chunk_wd_alt = {}

        #find alternative of each word
        for wd, wd_rt in zip(long_chunk_hnd, long_chunk_hnd_root):
            long_chunk_wd_alt[wd] = [wd]
            for i in range(1, len(ch)):
                tmp_root = [dic_root[l] if l in dic_root else l for l in ch[i][2]]
                if wd not in ch[i][2] and  wd_rt in tmp_root:
                    indx = tmp_root.index(wd_rt)
                    wd_alt = ch[i][2][indx]
                    if wd_alt not in long_chunk_wd_alt[wd]:
                        long_chunk_wd_alt[wd].append(wd_alt)

        ch.append(long_chunk_wd_alt)


    #FIRST ITERATION
    #for aligning smaller chunks inside long chunk
    for key in group_chunk:
        align_wds = {}
        align_eng_wds = [] #listof eng wds aligned
        align_hnd_wds = [] # list of hnd wds aligned
        ch = group_chunk[key]
        dic_wd_alt = ch[-1]
        for i in range(len(ch)-2, -1, -1):
            tmp_hnd = ch[i][3]
            tmp_eng = ch[i][1]
            tmp_eng_wd_id = ch[i][2]
            #if single word present in eng and hnd
            if(len(tmp_hnd) == 1) and (len(tmp_eng) == 1):
                tmp_hnd_wd = tmp_hnd[0]
                tmp_eng_wd_id = tmp_eng_wd_id[0]
                for key4 in dic_wd_alt:
                    if tmp_hnd_wd in dic_wd_alt[key4]:
                        if tmp_eng_wd_id not in align_wds:
                            align_wds[tmp_eng_wd_id] = [key4]
                            align_eng_wds.append(tmp_eng_wd_id)
                            align_hnd_wds.append(key4)
                        else:
                            align_wds[tmp_eng_wd_id].append(key4)
                            align_eng_wds.append(tmp_eng_wd_id)
                            align_hnd_wds.append(key4)
            else:
                #if single word in only eng side
                if(len(tmp_eng) == 1):
                    tmp_eng_wd_id = tmp_eng_wd_id[0]
                    for wd in tmp_hnd:
                        for key1 in dic_wd_alt:
                            if wd in dic_wd_alt[key1]:
                                if tmp_eng_wd_id not in align_wds and key1 not in align_hnd_wds:
                                    align_wds[tmp_eng_wd_id] = [key1]
                                    align_eng_wds.append(tmp_eng_wd_id)
                                    align_hnd_wds.append(key1)
                                else:
                                    align_wds[tmp_eng_wd_id].append(key1)
                                    align_eng_wds.append(tmp_eng_wd_id)
                                    align_hnd_wds.append(key1)

                #multiple words in both sides but number of eng and hnd are same
                elif(len(tmp_eng) == len(tmp_hnd)):
                    ids_aligned = []
                    ids_not_aligned = []
                    hnd_wds_aligned = []
                    hnd_wds_aligned1 = []

                    for id in tmp_eng_wd_id:
                        if id in align_wds:
                            ids_aligned.append(id)
                        else:
                            ids_not_aligned.append(id)

                    for k in align_wds:
                        hnd_wds_aligned.append(align_wds[k])

                    for sublist in hnd_wds_aligned:
                        for l in sublist:
                            hnd_wds_aligned1.append(l)
                    hnd_wds_not_aligned = list(set(tmp_hnd) - set(hnd_wds_aligned1))

                    '''
                    #for wds aligned list is empty then aligen all the words
                    if len(ids_aligned) == 0:
                        for id, wd_hnd in zip(tmp_eng_wd_id, tmp_hnd):
                            align_wds[id] = [wd_hnd]
                    '''
                    if len(ids_not_aligned) == 1 and len(hnd_wds_not_aligned) == 1:
                        align_wds[ids_not_aligned[0]] = hnd_wds_not_aligned[0]


        #change ids to string (e.g 15 to '15') for
        #further storing multiple ids '1_2_3'
        align_wds1 = {}
        for key5 in align_wds:
            align_wds1[str(key5)] = align_wds[key5]
        ch.append(align_wds1)

    # TODO
    # remove punctuations from hnd words before storing in align_wds

    #SECOND ITERATION
    #do a second iteration for aligning chunks where number words are different in both sides
    for key in group_chunk:
        ch = group_chunk[key]
        dic_wd_alt = ch[-2]
        align_wds = ch[-1]
        align_wds_ids = []
        for i in range(len(ch)-3, -1, -1):

            #to add multiple id (e.g. '1_2_3' to the total list of align wds
            for key1 in align_wds:
                tmp_ids = str(key1).split('_')
                if(len(tmp_ids) > 1):
                    for tmp_id in tmp_ids:
                        if int(tmp_id) not in align_wds_ids:
                            align_wds_ids.append(int(tmp_id))
                else:
                    if int(tmp_ids[0]) not in align_wds_ids:
                        align_wds_ids.append(int(tmp_ids[0]))



            # flag_process = 0
            # for id in ids:
            #     if id not in align_wds_ids:
            #         flag_process = 1
            #         break
            # #not required since the whole phrase is taken
            #if any word is not present in our align_wds dictionary then try to align using other align words
            # if(flag_process):
            #     found_id = []
            #     found_hnd = []
            #     not_found_id = []
            #     for id in ids:
            #         if (id in align_wds_ids): # try aligning by finding found and not found words
            #             if str(id) in align_wds:
            #                 if set(align_wds[str(id)]).issubset(set(tmp_hnd)):
            #                     found_id.append(id)
            #                     if align_wds[str(id)][0] not in found_hnd:
            #                         found_hnd.append(align_wds[str(id)][0])
            #                 else:
            #                     if id not in not_found_id: not_found_id.append(id)
            #             else: # case where id is part of a chunk (e.g 1 is part of '1_2_3')
            #                 for key2 in align_wds:
            #                     if str(id) in key2:
            #                         found_id.append(id)
            #                         for wds in align_wds[key2]:
            #                             if wds not in found_hnd:
            #                                 found_hnd.append(align_wds[key2])
            #                     else:
            #                         if id not in not_found_id: not_found_id.append(id)
            #         else:
            #             if id not in not_found_id: not_found_id.append(id)
            #
            #     not_found_hnd = [x for x in tmp_hnd if x not in found_hnd]
            #     # not_found_hnd = list(set(tmp_hnd) - set(found_hnd))
            #     tmp_key_id = '_'.join(str(id) for id in not_found_id)

            ids = ch[i][2]
            chunk_name = ch[i][0]
            tmp_eng = ch[i][1]
            tmp_hnd = ch[i][3]

            if('NP' in chunk_name):
                tmp_key_id = '_'.join(str(id) for id in ids)
                if tmp_hnd[0] != 'no_translation':
                    align_wds[tmp_key_id] = tmp_hnd
                    for id in ids:
                        if id not in align_wds_ids:
                            align_wds_ids.append(id)

        ch.append(list(set(align_wds_ids)))


    #Create a list eng hnd list in sequence for storing the final alignment
    for key11 in group_chunk:
        ch = group_chunk[key11]
        eng_long_chunk = ch[0][1]
        start_id = ch[0][2][0]
        end_id = ch[0][2][-1]
        align_wds = ch[-2]
        align_wds_ids = ch[-1]
        found_eng_wd = []
        align_eng_hnd_list = []

        #start from the first word to last word
        for i in range(start_id, end_id+1):
            if i in align_wds_ids:
                if str(i) in align_wds:
                    if (i - start_id < len(eng_long_chunk)):  # temporary fix for sent e.g 0007 'tackled solved'
                        tmp_eng = eng_long_chunk[i-start_id]
                        tmp_hnd = align_wds[str(i)]
                        found_eng_wd.append(i)
                        chunk_name = align_wds[str(i)]
                        align_eng_hnd_list.append([str(i), tmp_eng, tmp_hnd])
                        # align_wds[str(i)].append(tmp_eng)

                else: #for multiple id cases (e.g. 1_2_3 ) search the align_wds dic
                    for key12 in align_wds:
                        tmp_ids = key12.split('_')
                        if(len(tmp_ids)) > 1:
                            if str(i) in tmp_ids:
                                tmp_eng_list = []
                                tmp_hnd = align_wds[key12]
                                for id in tmp_ids:
                                    if(int(id) - start_id < len(eng_long_chunk)): # temporary fix for sent e.g 0007 'tackled solved'
                                        tmp_eng_list.append(eng_long_chunk[int(id) - start_id])
                                        found_eng_wd.append(int(id))

                                align_eng_hnd_list.append([key12, tmp_eng_list, tmp_hnd])
                                # align_wds[key12].append(tmp_eng_list)
                                break


            else: #if no alignment , then keep it empty
                if (i - start_id < len(eng_long_chunk)):  # temporary fix for sent e.g 0007 'tackled solved'
                    tmp_eng = eng_long_chunk[i - start_id]
                    align_eng_hnd_list.append([i, tmp_eng, ['empty']])
        ch.append(align_eng_hnd_list)




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
