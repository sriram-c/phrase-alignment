import  sys
import  os
import string
import re

anu_path = '/home/sriram/alignment/anusaaraka'
setu_path = '/home/sriram/Alignment/new-approach-alignment/hnd-morph/sampark'

with open(sys.argv[1], 'r')as f:
    cont = f.readlines()

wds = []
for l in cont:
    for wd in l.strip().split():
        wds.append(wd)

wds_uniq = list(set(wds))

root_dic = {}

for wd in wds_uniq:
    path = os.getenv('HOME_anu_test')

    morph_command = 'echo ' + wd.strip(string.punctuation) + ' |  apertium-destxt | lt-proc -ca ' + anu_path + '/bin/hi.morf.bin | apertium-retxt'
    out=os.popen(morph_command).readlines()
    for mo in out:
        if '*' not in mo:
            analysis = mo.split('/')
            for item in analysis:
                if '<' in item:
                    rt = re.findall(r'[^<]+<cat', item)
                    rt1 = rt[0][:-4]
                    if wd not in root_dic:
                        root_dic[wd] = [rt1]
                    else:
                        if rt1 not in root_dic[wd]:
                            root_dic[wd].append(rt1)

        else:
            path = os.getenv('setu')
            f = open(setu_path + '/bin/sl/morph/hin/t' , 'w')
            f.write('1\t' + wd.strip(string.punctuation)+'\n')
            sam_m_comm = 'sh ' + setu_path + '/bin/sl/morph/hin/morph_run.sh ' + setu_path + '/bin/sl/morph/hin/t'
            f.close()

            m_out=os.popen(sam_m_comm).readlines()
            if(len(m_out) != 0):
                r = m_out[0].split('\t')
                mo = r[3].split('|')
                for anal in mo:
                    r_lst = anal.split(',')
                    rt = r_lst[0][8:]
                    if wd not in root_dic:
                        root_dic[wd] = [rt]
                    else:
                        if rt not in root_dic[wd]:
                            root_dic[wd].append(rt)
                    print('inside', root_dic)


print(root_dic)
