# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
# importing the module
import datetime
import logging


import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt

import config
from src import util
# from src import click_event_util

import matplotlib.pyplot as plt
import streamlit as st


if "font_position_dict" not in st.session_state:
    st.session_state.font_position_dict = {
        'Text 1': [0, 0],
        'Text 2': [0, 0],
        'Text 3': [0, 0],
        'Text 4': [0, 0]
    }

def font_position_onchange():
    st.session_state.font_position_dict[font_position] = [st.session_state.col_slider, st.session_state.row_slider]

LINE = """<style>
    .vl {
    border-left: 2px solid black;
    height: 100px;
    position: absolute;
    left: 50%;
    margin-left: -3px;
    top: 0;
    }
    </style>
    <div class="vl"></div>"""

# Constants
MAX_IMAGE = 5
stroke_color = (0, 0, 0) 
font_color = (255, 255, 255)

if __name__ == "__main__":
    st.set_page_config(page_title='Political Meme Generator (IPMG)',
                page_icon=":chart_with_upwards_trend:",
                layout='wide', initial_sidebar_state='collapsed')



    st.title('Political Meme Generator (IPMG)', )
    st.subheader('IPMG is best way to create Indian Political Memes. Just for Fun.', )

    # Calculating Yesterday date
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    logging.info(f'Processing for Date: {current_date}')

    util.check_dir('uploaded_data')
    col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 10, 5, 5, 1])
    query_params = st.experimental_get_query_params()

    path_image = util.list_list('data', ('jpg', 'jpeg', 'png'))
    print(f'Number of Image found: {len(path_image)}')

    col6.write("**[Linkedin](https://www.linkedin.com/in/manishsahuiitbhu/)<br>\
                        [:beer:](https://rzp.io/i/K8x2gQ3wG)**",
                    unsafe_allow_html=True)

    n = len(path_image)

    img = []
    checkbox = []
    with col1.container():
        page = st.number_input('Page Number', min_value=0, max_value=n//MAX_IMAGE, step=1, value=0)
        pick_img = col2.selectbox(f"Select Image", [i for i in range(1, MAX_IMAGE+1)])

        for i in range(MAX_IMAGE):
            img = Image.open(path_image[int((page * MAX_IMAGE + i)%n)])
            img = img.resize((100, 100))
            st.image(img, use_column_width=True)
            # checkbox.append(col2.checkbox(''))

    img_index = int((page * MAX_IMAGE + pick_img-1)%n)
    img = Image.open(path_image[img_index])
    shape = np.array(img).shape

    # col3.write('----------')
    if 'col_slider' not in st.session_state:
        st.session_state['col_slider'] = 7

    if 'row_slider' not in st.session_state:
        st.session_state['row_slider'] = 7

    if 'font_color' not in st.session_state:
        st.session_state['font_color'] = font_color

    if 'stroke_color' not in st.session_state:
        st.session_state['stroke_color'] = stroke_color


    col3.slider(label='Row Slide', min_value=0, 
                max_value=shape[1], value=7, 
                key='row_slider', 
                on_change=font_position_onchange)

    col3.slider(label='Column Slide', min_value=0, 
                max_value=shape[0], value=7, 
                key='col_slider',
                on_change=font_position_onchange)

    # Images Draw Tool
    d1 = ImageDraw.Draw(img)

    # use a truetype font
    font_color = col5.color_picker('Font Color', '#FFFFFF')
    stroke_color = col5.color_picker('Outline Color', '#000000')

    texts = ['Text 1', 'Text 2', 'Text 3', 'Text 4']
    font_position = col4.selectbox("Adjust Font Position", texts)

    # Font size slider
    col4.slider(label='Font Size', min_value=0, 
                max_value=100, value=40, 
                key='font_slider')

    text1 = col4.text_input('Text 1')
    text2 = col4.text_input('Text 2')

    col5.write('')
    col5.write('')
    col5.write('')

    text3 = col5.text_input('Text 3')
    text4 = col5.text_input('Text 4')

    font = ImageFont.truetype("src/PatuaOne-Regular.ttf", st.session_state.font_slider)

    print(st.session_state.font_position_dict)

    d1.text((st.session_state.font_position_dict['Text 1'][0], st.session_state.font_position_dict['Text 1'][1]),
            text1, fill=font_color, font=font, 
            stroke_width=1, stroke_fill=stroke_color)

    d1.text((st.session_state.font_position_dict['Text 2'][0], st.session_state.font_position_dict['Text 2'][1]),
            text2, fill=font_color, font=font, 
            stroke_width=1, stroke_fill=stroke_color)

    d1.text((st.session_state.font_position_dict['Text 3'][0], st.session_state.font_position_dict['Text 3'][1]),
            text3, fill=font_color, font=font, 
            stroke_width=1, stroke_fill=stroke_color)

    d1.text((st.session_state.font_position_dict['Text 4'][0], st.session_state.font_position_dict['Text 4'][1]),
            text4, fill=font_color, font=font, 
            stroke_width=1, stroke_fill=stroke_color)

    col3.image(img, use_column_width=True)



    st.write("**:beer: Buy me a [beer](https://rzp.io/i/K8x2gQ3wG)**")
    expander = st.expander("This app is developed by Manish Sahu.")
    expander.write(
        "Contact me on [Linkedin](https://www.linkedin.com/in/manishsahuiitbhu/)")
    expander.write(
        "The source code is on [GitHub](https://github.com/ManishSahu53/political-meme-generator)")