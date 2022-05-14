import os
import shutil
import requests
import streamlit as st
from style_algorithm import style_transfer
from PIL import Image
import numpy as np
st.set_page_config(page_icon=Image.open('media/logo.png'), layout="wide")
st.title('A Neural Algorithm of Artistic Style')
st.subheader('To transfer a style, just select the content image you want to change and select the style image which patterns you want to transfer')
st.write("Based on an article from arxiv: https://arxiv.org/pdf/1508.06576.pdf")

col1, col2 = st.columns(2)
with col1:
    mode_col1 = st.radio(
    "Loading mode",
    ('Loading from your device', 'Loading by link'), key="111")
    
    if mode_col1 == 'Loading from your device':
        uploaded_content = st.file_uploader("Choose a content image", type=["png", "jpg"])
        if uploaded_content is not None:
            st.image(uploaded_content, caption='Content image')
            img_content = Image.open(uploaded_content, mode='r').convert('RGB')

    else:
        content_url = st.text_input('Link field', 'Paste your URL to image')
        if content_url is not 'Paste your URL to image':
            try:
                response = requests.get(content_url, stream=True)
                with open('img_content.png', 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)

                    img_content = Image.open('img_content.png', mode='r').convert('RGB')
                    st.image(img_content, caption='Content image')
                del response
            except Exception as e:
                e = RuntimeError('Unavalible link')
                st.exception(e)

with col2:
    mode_col2 = st.radio(
    "Loading mode",
    ('Loading from your device', 'Loading by link'))
    
    if mode_col2 == 'Loading from your device':

        uploaded_style = st.file_uploader("Choose a style image", type=["png", "jpg"])
        if uploaded_style is not None:
            st.image(uploaded_style, caption='Style image')
            img_style = Image.open(uploaded_style, mode='r').convert('RGB')
    else:
        style_url = st.text_input('Link field', 'Paste your URL to image', key="222")
        if style_url is not 'Paste your URL to image':
            try:
                response = requests.get(style_url, stream=True)
                with open('img_style.png', 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)

                    img_style = Image.open('img_style.png', mode='r').convert('RGB')
                    st.image(img_style, caption='Style image')
                del response
            except Exception as e:
                e = RuntimeError('Unavalible link')
                st.exception(e)

     
intensity = st.radio(
    "Intensity",
    ('Low', 'Medium', 'High'))

if intensity == 'Medium':
    style_weight = 10000000
elif intensity == 'High':
    style_weight = 1000000000
else:
    style_weight = 100000

count_of_iterations = st.slider('We recommend one iteration of algorithm by default. With more iterations waiting time will increase', 1, 50, 1)
n_iters = count_of_iterations

if st.button('Generate') and img_style and img_content:
    progress_bar = st.progress(0)
    
    result = style_transfer(img_content, img_style, progress_bar, style_weight, n_iters)
    st.image(result)



