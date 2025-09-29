import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

# 메인 페이지
st.title('This is main page')
# 사이드바(왼쪽)
with st.sidebar:
    st.title('This is sidebar')
    side_option=st.multiselect(
        label='Your selection is',
        options=['Car', 'Airplane', 'Train', 'Ship', 'Bicycle'],
        placeholder='select transportation' 
    )
img2 = Image.open(r'input\image2.jpg')
img3 = Image.open(r'input\image3.jpg')

st.header('Lemonade')
st.image(img2, width=300, caption='Image from Unsplash')
st.header('Cocktail')
st.image(img3, width=300, caption='Image from Unsplash')

# columns
col1, col2 = st.columns(2)
with col1:
    st.header('Lemonade')
    st.image(img2, width=300, caption='Image from Unsplash')
with col2:
    st.header('Cocktail')
    st.image(img3, width=300, caption='Image from Unsplash')   

st.divider()

# tab
tab1, tab2 = st.tabs(['Table', 'Graph'])
df = pd.read_csv(r'input\medical_cost.csv')
df = df.query('region == "northwest"')
with tab1:
    st.table(df.head(5))
with tab2:
    fig, ax = plt.subplots()
    # seaborn에 있는 산점도 그래프 사용
    # df의 bmi컬럼, charges컬럼, ax=축값
    sns.scatterplot(data=df, x='bmi', y='charges', ax=ax)
    st.pyplot(fig)
    