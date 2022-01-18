# 주식뉴스 크롤링 및 자연어처리 프로젝트


## Target

- 네이버 증권탭 주식종목별 뉴스 및 주가데이터를 2개월간 크롤링, 파이썬 라이브러리를 활용한 자연어처리 분석 

## Abstract

- 1. 크롤링
    - 1.주가 데이터 크롤링
    - 2.네이버 증권탭 종목별 뉴스 크롤링
    
    
- 2. 자연어처리 프로젝트
    - 1. konlpy를 활용한 주식뉴스 타이틀 워드클라우드
    - 2. 나이브베이즈를 활용한 주식뉴스 감성분석
    - 3. Word2vec을 활용한 주식 키워드 유사도분석


## 1. Data Crawling

#### 1-1. 주식 데이터 크롤링

- 상장된 주식 전 종목 일자별 크롤링
- 주요 컬럼 : 종목코드 / 종목이름 / 일자 / 종가 / 시장구분(코스닥 + 코스피)
- 기간 : 현시점부터 1년
- 크롤링 사이트 : http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020101

<img width="961" alt="스크린샷 2022-01-18 오후 7 49 31" src="https://user-images.githubusercontent.com/80455724/149926434-5d540329-45c2-4721-97c1-1775b714d324.png">



#### 1-2 네이버 증권탭의 종목관련 뉴스 크롤링

<img width="1002" alt="스크린샷 2022-01-18 오후 7 50 20" src="https://user-images.githubusercontent.com/80455724/149926457-b44e1077-616d-429e-905e-073ffd50fea5.png">


- 각 종목 페이지의 뉴스탭에서 크롤링
- 종목코드를 url에 대입하여 상장된 모든 기업의 뉴스를 크롤링
- 해당 이슈를 주가와 연계하기 위해서 뉴스의 게시 날짜를 함께 크롤링

## 2. 자연어처리 프로젝트

### 2-1 konlpy를 활용한 주식뉴스 타이틀 워드클라우드

<img width="1097" alt="스크린샷 2022-01-18 오후 8 02 11" src="https://user-images.githubusercontent.com/80455724/149926494-84132781-939c-4ecd-9da9-a0db3bcf773f.png">

- Konlpy.Okt를 활용하여 명사를 추출한 후, Stopwords를 설정하여 불용어를 제거, Text메서드를 활용하여 간단한 분석
 <img width="1302" alt="스크린샷 2022-01-18 오후 8 03 16" src="https://user-images.githubusercontent.com/80455724/149927124-78181944-7ae0-42c8-95e2-28ed5fcc4b2b.png">

- 워드클라우드를 import하여 빈도를 기준으로 워드클라우드를 그려보았다.

<img width="1323" alt="스크린샷 2022-01-18 오후 8 04 16" src="https://user-images.githubusercontent.com/80455724/149927335-6b011a7d-e9a0-461a-8a2f-a01655a204bf.png">

<img width="1138" alt="스크린샷 2022-01-18 오후 8 04 22" src="https://user-images.githubusercontent.com/80455724/149927347-07daae50-b3bc-418f-b6d2-2f005bf7d518.png">



### 2-2 나이브베이즈를 활용한 주식뉴스 감성분석

- 주가의 등락을 바탕으로 뉴스의 감성분석을 실시하기 위해, 주가데이터의 등락을 나타내는 컬럼을 추가해주었다.

<img width="838" alt="스크린샷 2022-01-18 오후 8 05 24" src="https://user-images.githubusercontent.com/80455724/149927645-8cfdeb40-2a40-4f3c-bacb-474d0a6f2947.png">

- 주가데이터와 주식뉴스데이터의 date컬럼을 전처리하여, 종목코드와 날짜를 바탕으로 left join하였음.

<img width="843" alt="스크린샷 2022-01-18 오후 8 05 37" src="https://user-images.githubusercontent.com/80455724/149927796-976ee970-5d50-461e-8168-736ef0375163.png">

- 해당 데이터셋을 바탕으로 train_test_split으로 데이터를 나눈 후, tf-idf벡터라이즈하여 나이브베이즈로 학습시켜 뉴스타이틀을 바탕으로 주식의 등락을 예측해보았음.

<img width="1005" alt="스크린샷 2022-01-18 오후 8 05 49" src="https://user-images.githubusercontent.com/80455724/149928041-26ca7da9-d19b-4d68-b9d1-ab3b8f699616.png">

-생각보다 잘맞다싶었지만, accuracy는 만족스럽지 못한 결과가 나왔다.

<img width="374" alt="스크린샷 2022-01-18 오후 8 06 02" src="https://user-images.githubusercontent.com/80455724/149928115-cfd40b5e-daac-4e95-b393-7d5ca21ca5fe.png">

- 아쉬운 점: 주가의 등락률을 상승,보합,하락으로 삼중 분류하여, 나이브베이즈에 학습시켰다면, 좀 더 정확하지 않을까.



### 2-3 Word2vec을 활용한 주식 키워드 유사도분석

- 상기와 같은 데이터를 활용하여, 형태소를 추출하고 조사,어미, 접사를 제거하는 전처리과정을 거침

<img width="542" alt="스크린샷 2022-01-18 오후 8 06 31" src="https://user-images.githubusercontent.com/80455724/149928435-58d49a22-58a8-4f4a-9813-c7cd51f34979.png">

- gensim의 word2vec을 활용하여, 특정키워드와 유사한 키워드를 뽑아보았다.

<img width="751" alt="스크린샷 2022-01-18 오후 8 07 13" src="https://user-images.githubusercontent.com/80455724/149928561-079edde0-6a88-4952-b53d-aae439947d19.png">

<img width="784" alt="스크린샷 2022-01-18 오후 8 07 58" src="https://user-images.githubusercontent.com/80455724/149928579-872cbbf7-c13b-4b48-8ef6-44819bebdcaa.png">



## 3. File 설명
---
