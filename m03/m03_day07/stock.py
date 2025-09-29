import streamlit as st
import datetime
import pandas as pd
import FinanceDataReader as fdr 
import plotly.graph_objects as go
import unicodedata 
# python -m pip install finance-datareader
# streamlit -> 페이지 설정(타이틀)
st.set_page_config(page_title='주식 차트 대시보드', page_icon='〽️')
st.title('〽️KOSPI 주식 차트 대시보드')

# 문자열 정규화 함수 -> 한글 종목명 띄어쓰기/특수문자 문제를 방지
def normalize_str(s):
    return unicodedata.normalize('NFKC', s).strip()

# KOSPI 시장 전체 종목 정보 가져오기
market = 'KOSPI'
df_market = fdr.StockListing(market) # 코스피 종목 가져와서 저장
df_market['Name'] = df_market['Name'].apply(normalize_str) # 종목명 정규화
stocks = df_market['Name'].tolist() # 종목명 리스트 추출

# 차트(막대그래프)
top10 = df_market.nlargest(10, 'Marcap').iloc[::-1] # 상위 10개 시가총액 역순(막대그래프 수평 정렬을 위해)
# iloc[::-1] -> -1씩 증가 (= 하나씩 거꾸로 읽어들이기)
fig = go.Figure(go.Bar(
    x=top10['Marcap']/1e12, # 시가총액을 '조'단위로 변환
    y=top10['Name'], 
    orientation='h', # 수평 막대그래프
    text=top10['Marcap']/1e12, # 그래프에 표시되는 텍스트(조 단위)
    texttemplate='%{text:.1f}조' # 텍스트 포맷 지정(소수점 1자리)
))
fig.update_layout(
    title='KOSPI 시가 총액 TOP10', # 차트제목
    xaxis_title='시가총액 (조)', # x축 제목
    yaxis_title='종목명', # y축 제목
    bargap=0.15 # 막대 간 간격 조정
)
st.plotly_chart(fig)

# 사이드바에서 종목 선택(최대 10개)
selected_stocks = st.sidebar.multiselect(
    '종목을 선택하세요 (최대 10개)', 
    stocks, # 종목명 리스트 추출한 것
    max_selections=10 # 최대 선택 가능 개수 제한
)
# 선택 종목명도 정규화(위에서 만든 정규화 함수 호출)
# -> 리스트 컴프리헨션(리스트 내포) -> for를 적용시켜 결과를 리스트로
selected_stocks = [normalize_str(s) for s in selected_stocks] 

# 선택된 종목명을 코드로 변환
codes = []
for name in selected_stocks:
    matched = df_market.loc[df_market['Name']==name, 'Code'].values 
    # name이 df_market의 이름과 같다면 code 값만 matched에 저장
    st.sidebar.write(f'선택 : {name} -> 코드 : {matched}') 
    if len(matched) > 0: # 선택한 것이 있다는 뜻이나 코드리스트에 추가
        codes.append(matched[0])

# 선택한 종목 코드가 없으면 경고 후 실행 중지
if not codes:
    st.warning('종목 코드를 찾을 수 없습니다. 종목을 다시 선택해주세요.')
    st.stop()

# 날짜 입력 -> 시작일(2022년 1월 1일), 종료일(오늘 날짜) -> 기본값으로 설정
start_date = st.sidebar.date_input('시작 날짜', datetime.date(2022, 1, 1))
end_date = st.sidebar.date_input('종료 날짜', datetime.datetime.now().date())

# 주식 데이터 불러오는 함수(예외처리 포함)
def get_stock_data(code, start, end):
    try: # 예외(오류)가 발생할 가능성이 있는 경우에 넣는다
        df = fdr.DataReader(code, start, end)
        if df.empty:
            return None # 데이터가 비었으면 None (없다 반환)
        return df # 데이터가 있다면 df 내용을 반환
    except Exception as e: # 예외메세지를 e라고 부르겠다
        st.error(f'{code} 데이터 로드 실패 : {e}') # 오류 메시지 출력
        return None

# 선택한 종목별 현재가와 변동폭(전일 대비) 표시
for i, code in enumerate(codes): # i : 인덱스 번호, code : 실제 값
    # 주식데이터를 불러온다(위에서 만든 함수 호출)
    df = get_stock_data(code, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
    if df is not None and len(df) >= 2: # 2개 이상일 경우
        current = df['Close'].iloc[-1] # 인덱스 번호 맨끝 -> 가장 최신 종가
        prev = df['Close'].iloc[-2] # 그 전일 종가
        delta = current - prev # 변동폭 계산
        # 화면에 종목명, 그 아래 최신 종가, 그 아래 변동폭
        st.metric(label=selected_stocks[i], value=f'{current:,}원', delta=f'{delta:,}원')
    else:
        st.warning(f'{selected_stocks[i]} 데이터가 충분하지 않습니다.') 

# 탭 -> 그래프가 나오도록 라인차트와 캔들스틱 차트 
tab1, tab2 = st.tabs(['라인 차트', '캔들스틱 차트'])

with tab1:
    if len(codes) == 1: # 종목을 하나만 선택했다면 차트도 하나만 출력
        df = get_stock_data(codes[0], start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
        if df is not None:
            st.line_chart(df['Close']) # 종가 라인 차트
        else:
            st.warning('데이터를 불러올 수 없습니다.')
    else: # 여러종목 선택했을 때 데이터 병합후 라인 차트 출력
        dfs = []
        for code in codes:
            df = get_stock_data(code, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
            if df is not None:
                df_temp = df[['Close']].rename(columns={'Close':code})
                dfs.append(df_temp)
        if dfs:
            merged_df = pd.concat(dfs, axis=1) # 수평방향으로 데이터프레임 병합
            merged_df.columns = selected_stocks # 컬럼명을 종목명으로 변경
            st.line_chart(merged_df)
        else:
            st.warning('선택한 종목의 데이터를 불러올 수 없습니다.')

with tab2: # 캔들스틱 차트 : 각 종목별 시가, 고가, 저가, 종가 표시
    for i, code in enumerate(codes):
        df = get_stock_data(code, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
        if df is not None:
            fig = go.Figure(data=[go.Candlestick(x=df.index, 
                                                 open=df['Open'], # 시가
                                                 high=df['High'], # 고가
                                                 low=df['Low'],  # 저가
                                                 close=df['Close'])]) # 종가
            fig.update_layout(title=f'{selected_stocks[i]} 캔들스틱 차트')
            st.plotly_chart(fig)
        else:
            st.warning(f'{selected_stocks[i]} 캔들스틱 차트를 불러올 수 없습니다.')