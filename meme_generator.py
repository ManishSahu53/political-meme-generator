# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
# importing the module
import os
import io
import datetime
import logging
import copy

import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt

import config
from src import util
from src import db_util
from src import io_util
from src.support_button import razor_button

# from src import click_event_util

import s3fs
import streamlit as st
import matplotlib.pyplot as plt
import streamlit.components.v1 as components  # Import Streamlit

# Create connection object.
# `anon=False` means not anonymous, i.e. it uses access keys to pull data.
fs = s3fs.S3FileSystem(anon=False)

if "font_position_dict" not in st.session_state:
    st.session_state.font_position_dict = {
        'Text 1': [0, 0],
        'Text 2': [0, 0],
        'Text 3': [0, 0],
        'Text 4': [0, 0]
    }

def font_position_onchange():
    st.session_state.font_position_dict[font_position] = [st.session_state.col_slider, st.session_state.row_slider]

# Constants
stroke_color = (0, 0, 0) 
font_color = (255, 255, 255)

# Connecting to Google Sheet
conn = db_util.GoogleSheet()

if __name__ == "__main__":
    st.set_page_config(page_title=config.title,
                page_icon=":chart_with_upwards_trend:",
                layout='wide', initial_sidebar_state='collapsed')


    st.title(config.title)
    st.subheader(config.sub_title)

    # Calculating Yesterday date
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    logging.info(f'Processing for Date: {current_date}')

    util.check_dir('uploaded_data')
    col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 10, 5, 5, 1])
    query_params = st.experimental_get_query_params()

    path_image = io_util.get_images(conn) # util.list_list('data', ('jpg', 'jpeg', 'png'))
    n = len(path_image)
    print(f'Number of Image found: {n}')

    img_list = []
    checkbox = []
    with col1.container():
        page = st.number_input('Page Number', min_value=0, max_value=n//config.MAX_IMAGE, step=1, value=0)
        pick_img = col2.selectbox(f"Select Image", [i for i in range(1, config.MAX_IMAGE+1)])

        for i in range(config.MAX_IMAGE):
            img = io_util.load_image(path_image[int((page * config.MAX_IMAGE + i)%n)])
            thumbnail_img = img.resize((100, 100))
            st.image(thumbnail_img, use_column_width=True)
            img_list.append(img)

    img_index = pick_img-1 # int((page * config.MAX_IMAGE + pick_img-1)%n)
    img_full = copy.deepcopy(img_list[img_index]) # io_util.load_image(path_image[img_index])
    shape = np.array(img_full).shape

    # col3.write('----------')
    if 'col_slider' not in st.session_state:
        st.session_state['col_slider'] = 10

    if 'row_slider' not in st.session_state:
        st.session_state['row_slider'] = 10

    if 'font_color' not in st.session_state:
        st.session_state['font_color'] = font_color

    if 'stroke_color' not in st.session_state:
        st.session_state['stroke_color'] = stroke_color


    col3.slider(label='Left Right Text Adjust', min_value=0, 
                max_value=shape[1], value=st.session_state.row_slider, 
                key='row_slider', 
                on_change=font_position_onchange)

    col3.slider(label='Up Down Text Adjust', min_value=0, 
                max_value=shape[0], value=st.session_state.col_slider, 
                key='col_slider',
                on_change=font_position_onchange)

    # Images Draw Tool
    d1 = ImageDraw.Draw(img_full)

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

    font = ImageFont.truetype(config.font_type, st.session_state.font_slider)

    # print(st.session_state.font_position_dict)

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

    col3.image(img_full, use_column_width=True)


    col6.write(f"**:beer: [Support]({config.support_url})**",
                unsafe_allow_html=True)

    # st.write(f"**:beer: [Support Me] ({config.support_url})**")
    st.write('')
    st.write('')
    components.html(razor_button.html_string)
    # Render the h1 block, contained in a frame of size 200x200.
    expander = st.expander("This app is developed by Manish Sahu.")
    expander.write(
        f"Contact me on [Linkedin]({config.linkedin_url})")
    expander.write(
        f"The source code is on [GitHub]({config.github_url})")
    
