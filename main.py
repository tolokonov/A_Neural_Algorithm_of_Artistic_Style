import streamlit as st
from PIL import Image
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
            pass
               
            #image = Image.open('sunrise.jpg')
            #st.image(image, caption='Sunrise by the mountains')

    else:
        content_url = st.text_input('Link field', 'Paste your URL to image')
        st.write('URL is correct')

with col2:
    mode_col2 = st.radio(
    "Loading mode",
    ('Loading from your device', 'Loading by link'))
    
    if mode_col2 == 'Loading from your device':

        uploaded_style = st.file_uploader("Choose a style image", type=["png", "jpg"])
        if uploaded_style is not None:
            pass

            #image = Image.open('sunrise.jpg')
            #st.image(image, caption='Sunrise by the mountains')
    else:
        style_url = st.text_input('Link field', 'Paste your URL to image')
        st.write('URL is correct')

     
intensity = st.radio(
    "Intensity",
    ('Low', 'Medium', 'High'))

if intensity == 'Medium':
    st.write('You selected medium intensity.')
else:
    st.write("You didn't select default intensity.")

    count_of_iterations = st.slider('We recommend one iteration of algorithm by default. With more iterations waiting time will increase', 1, 50, 1)
    st.write("I choose ", count_of_iterations, ' iterations')

if st.button('Generate') and uploaded_style and uploaded_content:
    pass
        #result = transfer_style(uploaded_content, uploaded_style)
        #st.image(result)
        #result.save(f'result_images/{str(random.randint(0, 10000))}.png')



