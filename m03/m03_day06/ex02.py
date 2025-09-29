import streamlit as st

# 슬라이더 -> 0부터 100까지의 점수, 기본값은 1
score = st.slider('Your score is ...', 0, 100, 1) # 0 ~ 100까지 1단위
# 입력받은 점수를 텍스트로 화면에 출력
st.text(f'Score : {score}')

st.divider()

# 시간 데이터를 다루기 위한 datetime표준 라이브러리 불러온다
from datetime import time

# 시작시간과 종료 시간을 슬라이더로 입력받는다
start_time, end_time = st.slider(
    'Working time is ...',
    min_value=time(0), # 최소시간 0시 -> 00:00
    max_value=time(23), # 최대시간 23시 -> 23:00(24시 기준) 
    value=(time(9), time(18)), # 기본값 09:00 ~ 18:00
    format='HH:MM' # 시간포맷을 시:분으로 표시
)
# 선택한 근무 시작시간과 종료시간을 텍스트로 출력
st.text(f'Working time : {start_time}, {end_time}')
