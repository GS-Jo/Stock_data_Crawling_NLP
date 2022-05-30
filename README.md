# 주식뉴스 크롤링 및 자연어처리 프로젝트

## Target
- 최근 Kospi지수가 3000을 넘어가며, 한국 국민들의 주식투자에 대한 관심이 크게 증가하고 있음.
- 주식개미들은 투자 의사결정을 위해 웹사이트의 증권뉴스를 주로 참고한다는 점에서 착안함.
- 주식뉴스데이터 및 주가데이터를 활용하여 다음과 같은 프로젝트를 진행해보고자 한다.

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


## 1. 데이터 

데이터 수집방법: 크롤링
활용툴: Sc

#### 1-1. 주가 데이터 크롤링

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


#### 아쉬운점 및 다음번을 위한 제언
- 주가데이터를 활용한 감성분석의 accuracy가 0.6으로 낮게 나온 점이 조금 아쉽다.
- 주가의 등락을 0,1로 할 것이 아니라, 주가의 등락률이 +-1%이내는 보합으로 추가하여 삼중분류로 분류기를 돌린다면 더 높은 accuracy가 나오지 않을까?

### 3. Word2vec을 활용한 주식 키워드 유사도분석

### 목표: 유사도분석을 통해 국내주식종목 및 주식테마의 관련키워드를 살펴보자!
- 활용데이터: 네이버증권 종목별 뉴스데이터

#### <결>
- gensim의 word2vec을 활용.
- 국내주식 메이저종목 및 테마와 관련키워드들을 살펴봄

<img width="1073" alt="스크린샷 2022-05-30 오후 6 38 12" src="https://user-images.githubusercontent.com/80455724/170964906-62c152c9-637f-455b-9a8d-d019320adb92.png">

