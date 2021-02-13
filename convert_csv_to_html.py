import re
import sys

pattern = '############\d+###########'

count = 0
count1 = 0
i = 0

print('<?xml version="1.0" encoding="UTF-8"?>' + '\n' + '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "">' + '\n' + '<html xmlns="http://www.w3.org/1999/xhtml">' + '\n' + '<head>' + '\n' + '<title>alignment</title>' + '\n' + '\n' + '</head>' + '\n' + '<body>')

for line in open(sys.argv[1]):
    i = 0
    result = re.match(pattern, line)
    if result:
            count1 = 0
            count1 = count1 + 1 
            count = count + 1
            print('</table>')
            print('</table>')
            print('<table border="1" cellspacing="0">')
            print('<tr><td> ' + str(count + 1) + '</td></tr>')
    else:        
        if count1 == 1 :
                print('<tr><td style="background-color:pink">')
                print('English_sen :: ' + line + '</td></tr>')
                count1 = count1 + 1 
        elif count1 == 2 :
                print('<tr><td style="background-color:lightgreen">')
                print('Hindi_sen :: ' + line + '</td></tr>')
                count1 = count1 + 1 
        elif count == 0 and count1 == 0:
                    print('<table border="1" cellspacing="0">')
                    print('<tr><td> ' + str(count + 1) + '</td></tr>')
                    print('<tr><td style="background-color:pink">')
                    print('English_sen :: ' + line + '</td></tr>')
                    count1 = 2
        else:           
                i = 0
                lst = line.strip().split('\t')
                for each in lst:
                    if i == 0 and count1 == 3:
                        print('<tr><table border="1" cellspacing="0">')
                        print('<td> ' + str(lst[i]) + '</td>')
                        i = i + 1
                        count1 = count1 + 1
                    else:
                        print('<td> ' + str(lst[i]) + '</td>')
                        i = i + 1
                print('</tr>')
                    

print ('</body>')
print ('</html>')
