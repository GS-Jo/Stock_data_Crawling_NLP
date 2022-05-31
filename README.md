# 주식뉴스 크롤링 & 자연어처리 프로젝트

## Target
- 스크래피를 활용한 주식뉴스 및 주가데이터 크롤링
- 수집한 주식뉴스데이터 및 주가데이터를 활용하여 다음과 같은 프로젝트를 진행해보고자함.

### (1) 증권뉴스 데이터와 주가데이터를 활용한 감성분석
- 특정일의 뉴스와 해당일 주식가격을 매치하여 특정뉴스가 게시된 날의 주가의 등락을 예측해보자.

### (2) Word2vec을 활용한 유사도분석
- 2021년 여름 한국주식시장의 핫한 키워드 찾아보기

## Abstract
- 1. 데이터수집
    - 1.주가 데이터 크롤링
    - 2.네이버 증권탭 종목별 뉴스 크롤링
    
- 2. 자연어처리 프로젝트
    - 1. 나이브베이즈를 활용한 주식뉴스 감성분석
    - 2. Word2vec을 활용한 주식 키워드 유사도분석

## 파일설명

### 데이터수집 파일

#### [주식뉴스 크롤링 및 자연어처리 프로젝트 주가데이터 크롤링](https://github.com/GS-Jo/Stock_data_Crawling_NLP/blob/main/%EC%A3%BC%EC%8B%9D%EB%8D%B0%EC%9D%B4%ED%84%B0_%ED%81%AC%EB%A1%A4%EB%A7%81.py)

#### [주식뉴스 크롤링 및 자연어처리 프로젝트 뉴스 크롤링](https://github.com/GS-Jo/Stock_data_Crawling_NLP/blob/main/%EC%A3%BC%EC%8B%9D%EB%89%B4%EC%8A%A4%20%ED%81%AC%EB%A1%A4%EB%A7%81.ipynb)

### 자연어처리 프로젝트 파일

#### [뉴스데이터와 주가데이터를 활용한 감성분석](https://github.com/GS-Jo/Stock_data_Crawling_NLP/blob/main/NLP_project/Stocknews_Sentiment.ipynb)

#### [뉴스데이터 Word2vec 유사도분석](https://github.com/GS-Jo/Stock_data_Crawling_NLP/blob/main/NLP_project/news_word2vec.ipynb)



# 1. 데이터 수집

데이터 수집방법: 크롤링
활용툴: Scrapy

#### 1-1. 주가 데이터 크롤링

<img width="961" alt="스크린샷 2022-01-18 오후 7 49 31" src="https://user-images.githubusercontent.com/80455724/149926434-5d540329-45c2-4721-97c1-1775b714d324.png">
- 크롤링 사이트 : http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020101

- 상장된 주식 전 종목 일자별 크롤링
- 주요 컬럼 : 종목코드 / 종목이름 / 일자 / 종가 / 시장구분(코스닥 + 코스피)
- 기간 : 현시점부터 1년

#### 1-2 네이버 증권탭의 종목관련 뉴스 크롤링

<img width="1002" alt="스크린샷 2022-01-18 오후 7 50 20" src="https://user-images.githubusercontent.com/80455724/149926457-b44e1077-616d-429e-905e-073ffd50fea5.png">

- 각 종목 페이지의 뉴스탭에서 크롤링
- 종목코드를 url에 대입하여 상장된 모든 기업의 뉴스를 크롤링
- 해당 이슈를 주가와 연계하기 위해서 뉴스의 게시 날짜를 함께 크롤링

# 2. 자연어처리 프로젝트

##  <나이브베이즈를 활용한 주식뉴스 감성분석>

## 예시: '광주 악몽 HDC현대산업개발, 7개월만에 또 사고…휘청' => 주가에 부정적
- 목표: 한국거래소 주가데이터와 네이버 종목별 뉴스데이터를 활용하여 특정 주식뉴스에 긍부정 나타내기
- 크롤링한 주가데이터를 활용하여 해당 뉴스가 개제된날의 주식 등락률을 0,1로 라벨링하여, 주식 뉴스 텍스트분석
- 나이브베이즈를 활용, 특정 신문기사를 입력했을 때 해당기사가 주가에 긍정적인가, 부정적인가를 예측하여 보자.

#### <결론>
- 주가의 등락을 바탕으로 뉴스의 감성분석을 실시하기 위해, 주가데이터의 등락을 나타내는 컬럼을 추가해주고.
<img width="838" alt="스크린샷 2022-01-18 오후 8 05 24" src="https://user-images.githubusercontent.com/80455724/149927645-8cfdeb40-2a40-4f3c-bacb-474d0a6f2947.png">

- tf-idf벡터라이즈한 후 나이브베이즈로 학습하여 뉴스타이틀을 바탕으로 주식의 등락을 예측해본 결과.

<img width="1005" alt="스크린샷 2022-01-18 오후 8 05 49" src="https://user-images.githubusercontent.com/80455724/149928041-26ca7da9-d19b-4d68-b9d1-ab3b8f699616.png">

화제성이 큰 뉴스에 대해서는 제법 정확하게 예측하는 것을 확인하였다.

<img width="1101" alt="스크린샷 2022-05-30 오후 6 33 47" src="https://user-images.githubusercontent.com/80455724/170963495-d74851e6-4d48-4e82-a6f9-e9488536d789.png">


#### 다음번을 위한 제언
- 주가의 등락을 0,1로 할 것이 아니라, 주가의 등락률이 +-1%이내는 보합으로 추가하여 삼중분류로 분류기를 돌린다면 더 높은 accuracy가 나오지 않을까?

## <Word2vec을 활용한 주식 키워드 유사도분석>

### 목표: 유사도분석을 통해 국내주식종목 및 주식테마의 관련키워드를 살펴보자!
- 활용데이터: 네이버증권 종목별 뉴스데이터

#### <결과>
- gensim의 word2vec을 활용.
- 국내주식 메이저종목 및 테마와 관련키워드들을 살펴봄

<img width="1073" alt="스크린샷 2022-05-30 오후 6 38 12" src="https://user-images.githubusercontent.com/80455724/170964906-62c152c9-637f-455b-9a8d-d019320adb92.png">


