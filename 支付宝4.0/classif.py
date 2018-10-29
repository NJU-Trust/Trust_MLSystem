import csv
import jieba
import jieba.analyse
from sklearn.feature_extraction.text import TfidfVectorizer
import random
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
medical = ['医院', '药店', '药', '健康']
canteen = ['九食', '星革见食', '大城小巷', '江南小镇']
live = ['携程网', '酒店', '住宿']
habit = ['账号' ,'游戏', '电影', '摄影', '舞', '画', '折纸', '书', '微博', '会员', '运动', '足球', '羽毛球', '乒乓球', '篮球', '健身', '博物馆']
invent = ['至余额宝', '买入', '定期理财', '转入']
iinvent = ['转出', '到银行卡', '赎回']
reward = ['收益发放']
huabei = ['花呗']
insurance = ['险', '红包', '收款', '转账']

jieba.load_userdict('./dict.txt')

# tfidf_csv_reader = csv.reader(open('tfidf.csv', 'r', encoding='utf-8'))
# tfidf_rows = [row for row in tfidf_csv_reader]
tfi = open('tfidf.txt','r', encoding='utf-8')
a = tfi.read()
tfi_dict = eval(a)
tfi.close()



cate = [ '1.1', '1.2', '1.3', '1.4', '2.2', '2.3', '2.4' , '4.1', '4.2', '5.1']
contents = []
# csv_reader = csv.reader(open('fil.csv', 'r', encoding='utf-8'))
# rows = [row for row in csv_reader]
for i in cate:
    csv_reader = csv.reader(open(i + '.csv', 'r', encoding='utf-8'))
    rows = [row for row in csv_reader]
    for j in range(0, len(rows)):
        contents.append([rows[j][0], rows[j][1]])
    # print(jieba.analyse.extract_tags(content, topK=1500, withWeight=True, allowPOS=())

random.shuffle(contents)
content = []
data_Y = []
for i in range(0, len(contents)):
    content.append(contents[i][0])
    data_Y.append(contents[i][1])
content.append('针织裙女2018新款韩版裙子秋季修身显瘦a字裙长袖针织连衣裙秋装')
content.append('雅思园快印南京南大店雅思园快印')

all_list= ['  '.join(jieba.cut(s,cut_all = False)) for s in content]
stpwrdpath ="./times.txt"
with open(stpwrdpath, 'rb') as fp:
    stopword = fp.read().decode('utf-8')  # 提用词提取
stopwordlist = stopword.splitlines()
tfidf=TfidfVectorizer(stop_words=stopwordlist)
train_X=tfidf.fit_transform(all_list)
# print(train_X[-1])
#
X_train, X_test, y_train, y_test = train_test_split(train_X[:-2], data_Y, test_size=0.10, random_state=33)
nb = MultinomialNB(alpha=1.0, fit_prior=True, class_prior=None)
nb.fit(X_train, y_train)
# y_predict = nb.predict(train_X[-2])
y_predict = nb.predict(X_test)

# print(y_predict)

print(classification_report(y_predict, y_test))