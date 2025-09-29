import streamlit as st

st.title('간단한 streamlit 퀴즈!')

# 1. 체크박스
agree = st.checkbox('Q1 파이썬은 프로그래밍 언어이다.(맞으면 체크)')
if agree: # 체크 O -> 값 존재 -> 참
    st.write('정답입니다!') # agree가 체크 O -> write구문 실행

st.divider()

# 2. 라디오 버튼 -> 하나만 선택 가능
person = st.radio(
    'Q2. 당신의 성별은 ??',
    ['남자', '여자']
)
if person == '남자':
    st.write('당신은 남자!')
else:
    st.write('당신은 여자!')

# 3. 단일 선택박스
transport = st.selectbox(
    'Q3. 가장 빠른 교통수단은??',
    ['기차', '자동차', '비행기', '배']
)
if transport == '비행기':
    st.write('정답! 비행기가 가장 빠릅니다!')
else:
    st.write('땡! 틀렸습니다. 비행기가 가장 빨라요 ~~')

# 4. 다중 선택 박스 
fruits = st.multiselect(
    '문제) 과일을 모두 선택하세요 (복수 정답 가능)',
    ['사과', '토마토', '당근', '바나나'] 
)
correct = {'사과', '토마토', '바나나'} # set

if set(fruits) == correct:
    st.write('완벽해요 모두 맞았습니다^^')
else:
    st.write('다시 선택해보세요!')