import streamlit as st
import pandas as pd
import datetime
import plotly.graph_objects as go # 대화형 그래프 생성
import FinanceDataReader as fdr # 주식 데이터를 가져오기 위한 라이브러리
import unicodedata # 유니코드 문자열 정규화

# 페이지 설정 : 타이틀과 파비콘 지정
st.set_page_config(page_title='주식 차트 대시보드', page_icon='📈')
st.title('KOSPI 주식 차트 대시보드 ')
