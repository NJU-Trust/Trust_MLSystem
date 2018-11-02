# -*- coding: utf-8 -*-

import csv
import os
import pandas as pd
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
import random
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import re
from pandas import DataFrame, Series
from urllib import request
from io import StringIO

def calculate_score(path):
    df = pd.read_csv(path)
    return round(df.iloc[3,1:].mean()*0.0488 + df.iloc[40,1:].mean() * 0.3 + df.iloc[41,1:].mean() * 0.5, 2)

def read_df(filename,time_col,money_col,type_col):
    df=pd.read_csv(os.path.join('./',filename),encoding='utf-8')
    print(os.path.join('./',filename))
    time = list(df.ix[:, time_col])
    #print(time)
    #time = pd.to_datetime(time)
    print(Series(df.ix[:, money_col]).astype('float'))
    temp_list = list(abs(Series(df.ix[:, money_col]).astype('float')))
    type= list(str(x) for x in df.ix[:, type_col])
    return [time,temp_list,type]



def form_basic_data(time,money,type):
    index = pd.MultiIndex.from_arrays([time, type], names=['time', 'type'])
    df = Series(money, index=index)
    grouped = df.groupby(level=['time', 'type'])
    df = grouped.sum()
    df = df.unstack()
    df.fillna(0,inplace=True)
    time = df.index
    time = pd.to_datetime(time)
    df = df.reindex(index=time)
    df = df.resample('M').sum()
    df.loc['Col_sum'] = df.apply(lambda x: x.sum())
    return df

def process_csv_data(alipay, card, username):
    ali_list=read_df(alipay,5,10,17)
    campus_list=read_df(card,3,4,6)
    ali_list[0].extend(campus_list[0])
    ali_list[1].extend(campus_list[1])
    ali_list[2].extend(campus_list[2])
    df=form_basic_data(ali_list[0],ali_list[1],ali_list[2])
    #print(df.columns)
    df=df.reindex(columns=['0.0', '1.1', '1.2', '1.3', '1.4', '1.5', '1.6', '2.1', '2.2', '2.3',
       '2.4', '3.0', '4.1', '4.2', '5.1', '5.2', '6.1', '6.2', '6.3','6.4', '7.0',
       '8.1', '8.2'],)
    df.fillna(0,inplace=True)
    #df.to_csv(os.path.join(data_path,'result.csv'))
    print(df.columns)
    sum_cat={
    'income':['6.2','6.3','8.1'],
    'rigid':['1.2','1.3','1.4','1.5','2.1'],
    'daily':['1.1','1.2','1.3','1.4','1.5','1.6'],
    'food':['2.1','2.2','2.3','2.4'],
    'travel':['3.0','4.1','4.2'],
    'fun':['5.1','5.2'],
    'expense':['daily','food','travel','fun','8.2']
    }
    for i in sum_cat.keys():
        df[i]=df[sum_cat[i][0]]
        for j in range(len(sum_cat[i])):
            if j==0:
                continue
            else:
                df[i]=df[i]+df[sum_cat[i][j]]
    for i in ['daily','food','travel','fun']:
        name=i+'2all'
        df[name]=df[i]/df['expense']
    df['disc']=df['expense']-df['rigid']
    temp_list=list(df['7.0'][1:-1])
    temp_list.append(0)
    temp_list.append(max(temp_list))
    df['liability']=temp_list
    df['investment']=df['6.1']-df['6.2']+df['6.4']
    df['surplus']=df['income']-df['expense']
    asset_temp=df['surplus'].cumsum()
    asset_temp[-1]=asset_temp[-2]
    df['asset']=asset_temp
    df['engel']=df['food']/df['expense']
    df['rigid_ratio']=df['rigid']/df['expense']
    df['d2a_ratio']=df['liability']/df['asset']
    df['db_ability']=df['surplus']/df['liability']
    df['leverage']=df['asset']/df['liability']
    df['consump_ratio']=df['expense']/df['income']
    df['saving_ratio']=df['surplus']/df['income']
    df=df.T
    df.to_csv(os.path.join('./', username + '_final_result.csv'))
    return os.path.join('./', username + '_final_result.csv')



def school_card_process(path, username):
    jieba.load_userdict('./dict.txt')
    card_xls = pd.read_excel(path)

    texts = card_xls['交易终端'].values
    contents = []
    csv_reader = csv.reader(open('card_data.csv', 'r', encoding='utf-8'))
    rows = [row for row in csv_reader]
    for j in range(0, len(rows)):
        contents.append([rows[j][0], rows[j][1]])
    random.shuffle(contents)
    content = []
    data_Y = []
    for i in range(0, len(contents)):
        content.append(contents[i][0])
        data_Y.append(contents[i][1])
    text_len = len(texts)
    for i in range(0, len(texts)):
        content.append(texts[i].replace('仙林', ''))
    all_list = ['  '.join(jieba.cut(s, cut_all=False)) for s in content]
    stpwrdpath = "./times.txt"
    with open(stpwrdpath, 'rb') as fp:
        stopword = fp.read().decode('utf-8')  # 提用词提取
    stopwordlist = stopword.splitlines()
    tfidf = TfidfVectorizer(stop_words=stopwordlist)
    train_X = tfidf.fit_transform(all_list)
    # X_train, X_test, y_train, y_test = train_test_split(train_X[:-2], data_Y, test_size=0.10, random_state=33)
    nb = MultinomialNB(alpha=1.0, fit_prior=True, class_prior=None)
    nb.fit(train_X[:-text_len], data_Y)
    y_predict = nb.predict(train_X[-text_len:])
    df = pd.DataFrame(data=y_predict, columns=['classification'])
    card_xls['classification'] = df
    card_xls.to_csv('./' + username + '_card.csv')
    return (username + '_card.csv')

def alipay_process(path, username):
    jieba.load_userdict('./dict.txt')
    alipay = open('./' + username + '_fil.csv', 'w', encoding='utf-8')
    up = 0
    bottom = 0
    data = request.urlopen(path).read().decode('ansi')
    data = StringIO(data)
    csv_reader = csv.reader(data)
    rows = [row for row in csv_reader]
    texts = []
    for i in range(0, len(rows)):
        if ((len(rows[i][0]) > 0)):
            if (str.isdigit(rows[i][0][0])):
                up = i
                break
    for i in range(len(rows) - 1, -1, -1):
        if (rows[i][0] != '') & (rows[i][0][0] == '-'):
            bottom = i
            break
    alipay.writelines(rows[up-1][0] + "," + rows[up-1][1] + "," + rows[up-1][2] + "," + rows[up-1][3] + "," + rows[up-1][4] + "," + rows[up-1][5] + "," + rows[up-1][6] + "," + rows[up-1][7] + "," + rows[up-1][8] + ',' + rows[up-1][9] + ',' + rows[up-1][10] + ',' + rows[up-1][11] + ',' + rows[up-1][12] + ',' + rows[up-1][13] + ',' + rows[up-1][14] + ',' + rows[up-1][15] + '\n')
    for i in range(up, bottom + 1):
        if ((len(rows[i][16]) > 0)):
            texts.append([rows[i][7] + rows[i][8], rows[i][15]])
            # fp.writelines(rows[i][7] + rows[i][8] + ',' + rows[i][16] + '\n')
            alipay.writelines(rows[i][0] + "," + rows[i][1] + "," + rows[i][2] + "," + rows[i][3] + "," + rows[i][4] + "," + rows[i][5] + "," + rows[i][6] + "," + rows[i][7] + "," + rows[i][8] + ',' + rows[i][9] + ',' + rows[i][10] + ',' + rows[i][11] + ',' + rows[i][12] + ',' + rows[i][13] + ',' + rows[i][14] + ',' + rows[i][15] + '\n')
    alipay.close()
    for i in range(0, len(texts)):
        fil = re.compile(u'[^\u4e00-\u9fa5]+', re.UNICODE)
        texts[i][0] = fil.sub('', texts[i][0])


    medical = ['医院', '药店', '药', '健康']
    canteen = ['九食', '星革见食', '大城小巷', '江南小镇']
    live = ['携程网', '酒店', '住宿']
    habit = ['账号', '游戏', '电影', '摄影', '舞', '画', '折纸', '书', '微博', '会员', '运动', '足球', '羽毛球', '乒乓球', '篮球', '健身', '博物馆']
    invent = ['至余额宝', '买入', '定期理财', '转入']
    iinvent = ['转出', '到银行卡', '赎回']
    reward = ['收益发放']
    huabei = ['花呗']
    insurance = ['险', '红包', '收款', '转账']

    non_type_i = []
    medical_i = []
    canteen_i = []
    live_i = []
    habit_i = []
    invent_i = []
    iinvent_i = []
    reward_i = []
    huabei_i = []
    insurance_i = []
    for i in range(0, len(texts)):
        if (texts[i][1].strip() == '') or (texts[i][1].strip() == '资金转移'):
            non_type_i.append(i)
        for j in huabei:
            if texts[i][0].__contains__(j):
                huabei_i.append(i)
        for j in insurance:
            if texts[i][0].__contains__(j):
                insurance_i.append(i)
        for j in reward:
            if texts[i][0].__contains__(j):
                reward_i.append(i)
        for j in iinvent:
            if texts[i][0].__contains__(j):
                iinvent_i.append(i)
        for j in invent:
            if texts[i][0].__contains__(j):
                invent_i.append(i)
        for j in habit:
            if texts[i][0].__contains__(j):
                habit_i.append(i)
        for j in live:
            if texts[i][0].__contains__(j):
                live_i.append(i)
        for j in canteen:
            if texts[i][0].__contains__(j):
                canteen_i.append(i)
        for j in medical:
            if texts[i][0].__contains__(j):
                medical_i.append(i)
    contents = []
    csv_reader = csv.reader(open('alipay_data.csv', 'r', encoding='utf-8'))
    rows = [row for row in csv_reader]
    for j in range(0, len(rows)):
        contents.append([rows[j][0], rows[j][1]])
    random.shuffle(contents)
    content = []
    data_Y = []
    for i in range(0, len(contents)):
        content.append(contents[i][0])
        data_Y.append(contents[i][1])
    text_len = len(texts)
    for i in range(0, len(texts)):
        content.append(texts[i][0])
    all_list = ['  '.join(jieba.cut(s, cut_all=False)) for s in content]
    stpwrdpath = "./times.txt"
    with open(stpwrdpath, 'rb') as fp:
        stopword = fp.read().decode('utf-8')
    stopwordlist = stopword.splitlines()
    tfidf = TfidfVectorizer(stop_words=stopwordlist)
    train_X = tfidf.fit_transform(all_list)
    # X_train, X_test, y_train, y_test = train_test_split(train_X[:-2], data_Y, test_size=0.10, random_state=33)
    nb = MultinomialNB(alpha=1.0, fit_prior=True, class_prior=None)
    nb.fit(train_X[:-text_len], data_Y)
    y_predict = nb.predict(train_X[-text_len:])
    for i in range(0, len(huabei_i)):
        y_predict[huabei_i[i]] = '7.0'
    for i in range(0, len(iinvent_i)):
        y_predict[iinvent_i[i]] = '6.2'
    for i in range(0, len(reward_i)):
        y_predict[reward_i[i]] = '6.3'
    for i in range(0, len(invent_i)):
        y_predict[invent_i[i]] = '6.1'
    for i in range(0, len(habit_i)):
        y_predict[habit_i[i]] = '5.2'
    for i in range(0, len(live_i)):
        y_predict[live_i[i]] = '3.0'
    for i in range(0, len(canteen_i)):
        y_predict[canteen_i[i]] = '2.1'
    for i in range(0, len(medical_i)):
        y_predict[medical_i[i]] = '1.5'
    for i in range(0, len(insurance_i)):
        if rows[insurance_i[i]][1].strip() == '已支出':
            y_predict[insurance_i[i]] = '8.2'
        if rows[insurance_i[i]][1].strip() == '已收入':
            y_predict[insurance_i[i]] = '8.1'
    for i in range(0, len(non_type_i)):
        y_predict[non_type_i[i]] = '0.0'

    alipay = pd.read_csv('./' + username + '_fil.csv')
    df = pd.DataFrame(data=y_predict, columns=['classification'])
    print(y_predict)
    alipay['classification'] = df
    alipay.to_csv('./' + username + '_alipay.csv')
    # fp.close()
    return username + '_alipay.csv'

