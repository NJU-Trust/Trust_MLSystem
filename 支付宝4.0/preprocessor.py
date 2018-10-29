import csv
import os
import re
fp = open("test.csv", 'w', encoding='utf-8')
up = 0
bottom = 0
for i in range(1, 16):
    csv_reader = csv.reader(open('alipay (' + str(i) + ').csv', 'r', encoding='ansi'))
    rows = [row for row in csv_reader]
    for i in range(0, len(rows)):
        if ((len(rows[i][0])>0)):
            if (str.isdigit(rows[i][0][0])):
                up = i
                break
    for i in range(len(rows)-1, -1, -1):
        if (rows[i][0] != '') & (rows[i][0][0] == '-'):
            bottom = i
            break
    for i in range(up, bottom+1):
        if ((len(rows[i][16]) > 0)):
            print(rows[i][16])
            fp.writelines(rows[i][7]+rows[i][8] + ',' + rows[i][16] + '\n')
fp.close()
csv_reader = csv.reader(open('test.csv', 'r', encoding='utf-8'))
fp = open("fil.csv", 'w', encoding='utf-8')
rows = [row for row in csv_reader]
for i in range(0, len(rows)):
    fil = re.compile(u'[^\u4e00-\u9fa5]+', re.UNICODE)
    rows[i][0] = fil.sub('', rows[i][0])
    fp.writelines(rows[i][0] + ',' + rows[i][1] + '\n')

