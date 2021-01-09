import sys
import ast
import re


def process_missing_ids(match_list_id, wds, longest, word_alt):
    swd = []
    lwd = []
    swd_org = []

    match_dic = {}
    for m in match_list_id:
        match_dic[m[0]] = m[1]

    for i in range(0,len(wds)):
        swd_org.append(i)

    for m in match_list_id:
        swd.append(m[0])
        lwd.append(m[1])

    perc = float(len(swd))/float(len(wds))

    if(perc > 0.5):
        print(wds)
        print(match_list_id)
        diff = list(set(swd_org)-set(swd))
        print('diff:',diff)

        for d in diff:
            if d-1 in swd:
                match_d = match_dic[d-1]+1
                print(d, match_d)
                print(wds[d], longest[match_d])
                if match_d in word_alt:
                    word_alt[match_d] = word_alt[match_d]+'/'+wds[d]
                else:
                    word_alt[match_d] = wds[d]
    else:
        print('wrong match')



def vibhakti_group(hnd):
    vib_list = ['ne','waka','kA', 'se', 'ko']
    hnd1 = []
    for wds in hnd:
        new_wds = wds.split()
        for i in range(0,len(wds.split())):
            wd_list = wds.split()
            if(wd_list[i] in vib_list):
                new_wds[i-1] = new_wds[i-1]+'_'+wd_list[i]
                new_wds[i] = 'empty'


        for w in new_wds:
            if w == 'empty':
                new_wds.remove(w)


        hnd1.append(' '.join(new_wds))
    return hnd1

with open(sys.argv[1], 'r')as f:
    cont = f.readlines()

with open(sys.argv[2], 'r')as f:
    cont_root = f.readlines()

dic_root = ast.literal_eval(cont_root[0])

hnd = []
for line in cont:
    hnd.append(line.split('\t')[1])

hnd1 = vibhakti_group(hnd)
print(hnd1)

longest = hnd1[1].split()


longest_root = []
for wd in longest:
    if wd in dic_root:
        longest_root.append(dic_root[wd])
    else:
        longest_root.append(wd)

tmp_id_str = []
for i in range(0, len(longest)):
    tmp_id_str.append([longest[i],i])

print(tmp_id_str)
print('--------')

word_alt = {}
for i in range(2,len(hnd1)):
    if hnd1[i] in longest:
        continue
    else:
        wds = hnd1[i].split()
        wds_root = []
        for wd in wds:
            if wd in dic_root:
                wds_root.append(dic_root[wd])
            else:
                wds_root.append(wd)

        match_list_id = []
        match_list = []

        for j in range(0, len(wds)):
            if wds[j] in longest:

                index = longest.index(wds[j])
                match_list_id.append([j,index])
                match_list.append([wds[j],index])

            elif wds_root[j] in longest_root:

                index = longest_root.index(wds_root[j])
                match_list_id.append([j,index])
                match_list.append([[wds[j],longest[index]],index])

                if index in word_alt and word_alt[index] != wds[j]:
                    word_alt[index] = word_alt[index]+'/'+wds[j]
                else:
                    word_alt[index] = wds[j]


        if(len(wds) != len(match_list_id)):
            process_missing_ids(match_list_id,wds,longest,word_alt)
        print('-------')

#print(tmp_id_str)
print(word_alt)




