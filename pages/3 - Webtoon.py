import streamlit as st
from PIL import Image

image = Image.open(r'/Users/jylee/streamlit.venv/bin/HackerTon_1111/pages/KakaoTalk_Photo_2023-11-12-03-44-15.png')

st.header('GLC 졸업요건 웹툰')
st.image(image, caption = '졸업 요건 웹툰')
