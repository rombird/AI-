import streamlit as st

# button
# 버튼을 클릭했을 때 
def button_write():
    st.write('버튼을 클릭했다!!!')
st.button('Reset', type='primary')
st.button('클릭했음', on_click=button_write) # on_click : 이벤트함수에서 함수호출시 ()생략

st.divider() # 구분선

if st.button('ㅋㅋㅋ'):
    st.write('ㅋㅋㅋ streamlit 수업중입니다!!')

st.divider()

# 중요 버튼
if st.button('중요 버튼', type='primary', key='btn1'):
    st.write('중요 버튼이 클릭되었습니다.')

# 보통버튼
if st.button('일반 버튼', type='secondary', key='btn2'):
    st.write('일반 버튼이 클릭되었습니다.')

# 버튼처럼 생기지 않음 -> 버튼 기능만(디자인만)
if st.button('무시', type='tertiary', key='btn3'):
    st.write('무시 버튼이 클릭되었습니다.')