import sys
import re
from bs4 import BeautifulSoup, Tag, NavigableString



def find_leaf(tag, phrase, flag):
    tmp_wd = []
    tmp_id = []

    if(flag):
        for wd in tag.find_all('leaf'):
            tmp_wd.append(wd['value'] + '_' + str(wd['id']))
        phrase.append([tag['value'] + str(tag['id']), tmp_wd])

    elif(tag['value'] == 'CC'):
        cc_wd = tag.find_all('leaf')[0]['value']

        if(len(list(tag.previous_siblings)) > 1):
            prev_sib = list(tag.previous_siblings)[1]
            prev_sib1 = prev_sib['value']+str(prev_sib['id'])
        else:
            prev_sib1 = 'NOT FOUND'

        if(len(list(tag.next_siblings)) > 1):
            next_sib = list(tag.next_siblings)[1]
            next_sib1 = next_sib['value'] + str(next_sib['id'])
        else:
            next_sib1 = 'NOT FOUND'

        phrase.append([tag['value']+str(tag['id']), prev_sib1, next_sib1, cc_wd])
        if(prev_sib1 != 'NOT FOUND'):
            find_leaf(prev_sib, phrase, 1)
        if(next_sib1 != 'NOT FOUND'):
            find_leaf(next_sib, phrase, 1)

    elif (re.match( r'^NP|NP-TMP|WHNP|NNS|PP|WHPP|ADJP|WHADJP|WHADVP|ADVP|WHAVP|X|SBAR|NAC|NML|CONJP|FRAG|INTJ|LST|NAC|NX|QP|PRC|PRN|PRT|QP|RRC|UCP|ROOT|S|,$', tag['value']) and (tag.name != 'leaf')):
        for wd in tag.find_all('leaf'):
                tmp_wd.append(wd['value']+'_'+str(wd['id']))
        phrase.append([tag['value']+str(tag['id']), tmp_wd])

def find_lwg(tag,tmp_lwg,flag):
    for tag1 in tag.contents:
        if (isinstance(tag1, Tag)):
            if (re.match(r'^VB|ADVP|RB|PRT|TO|MD', tag1['value'])):
                tmp_val = tag1.find_all('leaf')[0]['value']
                tmp_id = tag1.find_all('leaf')[0]['id']
                tmp_lwg.append(tmp_val+'_'+str(tmp_id))

            elif (re.match(r'^VP', tag1['value'])):
                find_lwg(tag1,tmp_lwg,1)
    if(flag == 0):
        phrase.append([tag['value']+str(tag['id'])+'_LWG', tmp_lwg])


def process_tag(tag, phrase):
        if (isinstance(tag, Tag)):
            if (tag['value'] == 'VP') and (tag.parent['value'] != 'VP'):
                tmp_lwg = []
                find_lwg(tag,tmp_lwg,0)
                for tag1 in tag.contents:
                    if (isinstance(tag1, Tag)):
                        process_tag(tag1, phrase)


            elif(re.match(r'CC',tag['value'])):
                find_leaf(tag, phrase, 0)

            else:
                find_leaf(tag, phrase, 0)
                for tag1 in tag.contents:
                    if (isinstance(tag1, Tag)):
                        process_tag(tag1, phrase)


with open(sys.argv[1]) as fp:
    soup = BeautifulSoup(fp, 'lxml-xml')

root = soup.find_all(value='ROOT')[0]


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
    if(isinstance(ch, Tag)):
        process_tag(ch,phrase)

phrase_dic = {}


count = 1
for p in phrase:
    if(re.match(r'CC',p[0])):
        phrase_dic[p[0]] = p[1]+'-'+p[3]+'-'+p[2]
    else:
        if p[0] not in phrase_dic:
            phrase_dic[p[0]] = ' '.join(p[1])

for key in phrase_dic:
    print(key,phrase_dic[key])
