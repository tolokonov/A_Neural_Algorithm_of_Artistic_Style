import streamlit as st
from PIL import Image
st.title('A Neural Algorithm of Artistic Style')
st.write("Based on an article from arxiv: https://arxiv.org/pdf/1508.06576.pdf")
uploaded_content = st.file_uploader("Choose a content image", type=["png", "jpg"])
if uploaded_content is not None:
    pass
    
    #image = Image.open('sunrise.jpg')
    #st.image(image, caption='Sunrise by the mountains')

uploaded_style = st.file_uploader("Choose a style image", type=["png", "jpg"])
if uploaded_style is not None:
    pass

    #image = Image.open('sunrise.jpg')
    #st.image(image, caption='Sunrise by the mountains')

intensity = st.radio(
     "Intensity",
     ('Low', 'Medium', 'High'))

if intensity == 'Medium':
     st.write('You selected medium intensity.')
else:
     st.write("You didn't select default intensity.")

count_of_iterations = st.slider('We reccomend one iteration of algorithm by default. With more iterations waiting time will increase', 1, 50, 1)
st.write("I choose ", count_of_iterations, ' iterations')

if st.button('Generate') and uploaded_style and uploaded_content:
    pass
    #result = transfer_style(uploaded_content, uploaded_style)
    #st.image(result)
    #result.save(f'result_images/{str(random.randint(0, 10000))}.png')



