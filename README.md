# Stock_data_Crawling_NLP


from google.colab import drive
drive.mount('/content/drive')
# !sudo apt-get install -y fonts-nanum
# !sudo fc-cache -fv
# !rm ~/.cache/matplotlib -rf
#apt로 나눔폰트설치
!apt-get update -qq
!apt-get install fonts-nanum* -qq
# 폰트지정
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

path = '/usr/share/fonts/truetype/nanum/NanumGothicEco.ttf'
font_name = fm.FontProperties(fname=path, size=10).get_name()
print(font_name)
plt.rc('font', family=font_name)
fm._rebuild()
#retina설정 - 뚜렷하게
import matplotlib.pyplot as plt
%config InlineBackend.figure_format = 'retina'

plt.title('안녕')
# konlpy & wordcloud 설치
!pip install konlpy wordcloud
import nltk
nltk.download('punkt')
#############################################################
#### 1. konlpy와 nltk를 활용한 주식뉴스 키워드 '워드클라우드' 만들기

import pandas as pd
import matplotlib.pyplot as plt
stock_news = pd.read_csv('/content/drive/MyDrive/Korean_Stock_Project/stock.csv')
stock_news

news_title = stock_news['title']
# 명사 추출 위해 타이틀 문자열로 바꿔 담기
title_list = [ str(a) for a in news_title]

# 리스트 제거하기
text = ''

for each in title_list:
  text = text + each + '\n'
# 형태소분석기 임포트
import nltk
from konlpy.tag import Okt

tf = Okt()
#명사 추출
title_tokens = tf.nouns(text)
title_tokens
## 단어의 등장빈도를 보자
# Text메서드에 넣어 활용해보자.
TT = nltk.Text(title_tokens)

print(len(set(TT.tokens)))
TT.vocab()
# stopword 설정하기
stop_words = ['.','(',')',',',"'",'%','-','X','[',']','의','자',
              '에','안','번','호','을','이','다','만','로','가','를',
              '금','중','시','사','치','새','숨','수','척','배','초',
              '기','더','온','전','임','위','무','손','판','과','년',
              '익','눈','나','날','점','젤','스','토','또','주','등',
              '제']

TT = [word for word in TT if word not in stop_words]
TT
# 빈도순 차트

tt = nltk.Text(TT)

plt.figure(figsize=(12,6))
tt.plot(50)
plt.show()
# 4차 산업혁명 키워드 - 얼마나 등장했을까?
keywords = ['IOT','사물인터넷','빅데이터','인공지능','AI','블록체인','암호화폐','NFT','3D 프린팅','모빌리티','드론','자율','주행','전기차','메타','버스','가상세계','ESG','친환경']

for word in keywords:
  print( f'{word} :', tt.count(word))


# 워드클라우드

%matplotlib inline

from matplotlib import font_manager, rc
plt.rcParams['axes.unicode_minus'] = False
path = '/usr/share/fonts/truetype/nanum/NanumGothicEco.ttf'

font_name = font_manager.FontProperties(fname=path).get_name()
rc('font',family=font_name)
from wordcloud import WordCloud

data = tt.vocab().most_common(200)

cloud = WordCloud(font_path=path, relative_scaling=0.2,
                  background_color='white').generate_from_frequencies(dict(data))

plt.figure(figsize=(16,12))
plt.imshow(cloud)
plt.axis('off')
plt.show()


###########################################################################
#### 2. 감성분석

# 크롤링한 주가데이터를 활용하여 해당 뉴스가 개제된날의 주식 등락률을 0,1로 라벨링하여, 주식 뉴스 텍스트분석
# 나이브베이즈를 활용, 특정 신문기사를 입력했을 때 해당기사가 주가에 긍정적인가, 부정적인가를 보여주는 감성분석 프로젝트

import pandas as pd

# 크롤링한 주식뉴스 데이터 및 주가데이터 불러오기

stock_news = pd.read_csv('/content/drive/MyDrive/Korean_Stock_Project/stock.csv')
stock_price = pd.read_csv('/content/drive/MyDrive/Korean_Stock_Project/데이터.csv',index_col=0)

stock_news = stock_news.drop(['news_link'],axis=1)
#날짜 컬럼 합치기 쉽게 전처리
character = '.: '

for a in range(len(character)):
  stock_news['date'] = stock_news['date'].str.replace(character[a],'')

stock_news['date'] = stock_news['date'].str.slice(start=0, stop=8)
stock_news = stock_news.astype({'date':'object'})
# 결측치 및 문제있는값 제거
idx = stock_news[stock_news['date']=='date'].index
stock_news.drop(idx,inplace=True)

stock_news = stock_news.dropna()
# 주가 등락 컬럼 추가
stock_price['GoodBad'] = [0. if value.find('-')== 0 else 1. for value in stock_price['FLUC_RT']]

GB = stock_price[['ISU_SRT_CD','DATE','GoodBad']]

GB = GB.rename(columns={'DATE':'date','ISU_SRT_CD':'stock_code'})
GB = GB.astype({'date':'string'})
GB = GB.astype({'date':'object'})

GB = GB.dropna()
# 날짜 데이터타입 변환
stock_news['date'] = pd.to_datetime(stock_news['date'])
GB['date'] = pd.to_datetime(GB['date'])
GB.info()
stock_news.info()
# 합치기
df = pd.merge(stock_news,GB,how='left',on=['date','stock_code'])
df
df['GoodBad'].value_counts()
# # df csv파일로 저장
# df.to_csv('./news_df.csv')
# 데이터 나누기
from sklearn.model_selection import train_test_split

text_train,text_test,class_train,class_test = train_test_split(df['title'],df['GoodBad'],test_size=0.2)
# 데이터타입 변경
text_train = text_train.values.astype('str')
text_test = text_test.values.astype('str')
# 벡터화
from sklearn.feature_extraction.text import CountVectorizer

count_vect = CountVectorizer()
train_count = count_vect.fit_transform(text_train)
train_count.shape
# tf-idf 변환
from sklearn.feature_extraction.text import TfidfTransformer

tf = TfidfTransformer(use_idf=False).fit(train_count)
train_tf = tf.transform(train_count)
train_tf.shape
# 나이브베이즈 분류기 학습
from sklearn.naive_bayes import MultinomialNB


multinb = MultinomialNB()

classifier = multinb.fit(train_tf, class_train)
# 테스트
# 2022.01.12 HDC 현대산업개발 아파트 붕괴사고 기사 - 주가 폭락
# 2022.01.12 sk하이닉스 기사 - 주가 상승
tt = ['광주 악몽 HDC현대산업개발, 7개월만에 또 사고…휘청','골드만·씨티·UBS 등 글로벌 IB의 잇단 반도체 긍정론…삼성전자·SK하이닉스 상승세 불 지펴']

tt_counts = count_vect.transform(tt)
tt_tf = tf.transform(tt_counts)

pred_tt = classifier.predict(tt_tf)

for text, gb in zip(tt, pred_tt):
  print('%r => %s' %(text, '주가에 긍정적' if gb == 1 else '주가에 부정적' ))
# 파이프라인

from sklearn.pipeline import Pipeline

pipe_clf = Pipeline([
                ('vect', CountVectorizer()),
                ('tfidf', TfidfTransformer()),
                ('clf', MultinomialNB()),
])
# 파이프라인 학습시키기
pipe_clf.fit(text_train,class_train)

# test데이터 예측하기
pred_test = pipe_clf.predict(text_test)
pred_test
## test_accuracy 확인
# 예상대로 낮은 수치
import numpy as np

np.mean(pred_test == class_test)

# 제언

- 주가의 등락을 0,1로 할 것이 아니라, 주가의 등락률이 +-1%이내는 보합으로 추가하여 삼중분류로 분류기를 돌린다면 더 높은 accuracy가 나오지 않을까?

################################################################

#### word2vec을 이용한 유사도분석 (목표: 4차혁명 관련 키워드 / 테마주 관련 키워드 분석)
import pandas as pd
import numpy as np

import gensim
from gensim.models import word2vec
news_df = pd.read_csv('./news_df.csv')
news_df
from konlpy.tag import Okt

tf = Okt()
# 정규표현식으로 필요없는 문자 제거
drop_text = '"[],.·→\''

for a in range(len(drop_text)):
  news_df['title'] = news_df['title'].str.replace(drop_text[a],"")
# 형태소 분해 및 조사, 어미, 접사 제거

result = []

for line in title_text:
  parts = tf.pos(line, norm=True, stem= True)
  a = []

  for word in parts:
    if not word[1] in ['Josa', 'Eomi', 'Punctuation']:
      a.append(word[0])

  core = (" ".join(a)).strip()
  result.append(core)
  print(core)
data_file = 'news_title.data'
# # 추출한 핵심 형태소파일 저장 
# with open(data_file, 'w', encoding='utf-8') as fp:
#   fp.write('\n'.join(result))
data = word2vec.LineSentence(data_file)
model = word2vec.Word2Vec(data, size=200, window=10, hs=1, min_count=2, sg=1)
# # 모델 저장
# model.save('news_title.model')

## 비슷한 단어를 찾아보자
# 삼성
# 2021년 여름, 삼성엔 호재보다는 악재가 많았던 듯 하다.
model.wv.most_similar(positive=['삼성'])
#하이닉스
model.wv.most_similar(positive=['하이닉스'])
# 메타버스

model.wv.most_similar(positive=['메타'])
# 엔씨소프트
model.wv.most_similar(positive=['엔씨소프트'])
