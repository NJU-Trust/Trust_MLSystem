import csv
import random
import codecs
import pandas
import re
import jieba
import numpy
import jieba.analyse
from sklearn.model_selection import train_test_split



categories = ['1.1', '1.2', '1.3', '1.4', '2.2', '2.3', '2.4', '4.1', '4.2', '5.1']

# out1 = open('alipay_train.txt', 'w', encoding='utf-8')
# out2 = open('alipay_val.txt', 'w', encoding='utf-8')
# out3 = open('alipay_test.txt', 'w', encoding='utf-8')
content = []
data_Y = []
for i in categories:
    csv_reader = csv.reader(open(i + '.csv', encoding='utf-8'))
    rows = [row for row in csv_reader]
    words = ''
    for j in range(0, int(len(rows))):
        if len(rows[j])==0:
            continue
        words += str(rows[j][0])
    print(jieba.analyse.extract_tags(words, withWeight=True, topK=10000).__len__())

    # random.shuffle(rows)
#     for j in range(0, int(len(rows))):
#         if len(rows[j])==0:
#             continue
#         if str(rows[j][0]) == '':
#             continue
#         content.append(rows[j][0])
#         data_Y.append(rows[j][1])
#
# X_train, X_test, y_train, y_test = train_test_split(content, data_Y, test_size=0.15, random_state=33)
# X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.15, random_state=33)
# print(X_val)
    # for j in range(int(len(rows) * 0.6), int(len(rows) * 0.8)):
    #     if len(rows[j])==0:
    #         continue
    #     if str(rows[j][0]) == '':
    #         continue
    #     out2.writelines(str(rows[j][1]) + '\t' + str(rows[j][0]) + '\n')
    # for j in range(int(len(rows) * 0.8), len(rows)):
    #     if len(rows[j])==0:
    #         continue
    #     if str(rows[j][0]) == '':
    #         continue
    #     out3.writelines(str(rows[j][1]) + '\t' + str(rows[j][0]) + '\n')