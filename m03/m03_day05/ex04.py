import streamlit as st
from PIL import Image

image = Image.open(r'm03_day05\dr.jpeg')
st.image(image)

st.divider()

st.image(image, caption='가로100', width=100) # 비율에 맞게 가로 100로 줄어든다

st.divider()

st.image(image, caption='가로200', width=200)