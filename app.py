# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
# importing the module

import os
import datetime
import traceback
import tempfile
import logging

import cv2
import numpy as np
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

import config
from src import util
from src import click_event_util

import plotly.express as px
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_drawable_canvas import st_canvas

st.set_page_config(page_title='Political Meme Generator (IPMG)',
                   page_icon=":chart_with_upwards_trend:",
                   layout='wide', initial_sidebar_state='collapsed')

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

# Constants for sidebar dropdown
SIDEBAR_OPTION_UPLOAD_IMAGE = "Upload an Image"
LOADING_TEXT = 'Please wait for model to detect hotspots. This can take few minutes. Hotspots can be from Solar or any other Image'

st.title('Political Meme Generator (IPMG)', )
st.subheader('IPMG is best way to create Indian Political Memes. Just for Fun.', )

# Calculating Yesterday date
current_date = datetime.datetime.now().strftime('%Y-%m-%d')
logging.info(f'Processing for Date: {current_date}')

util.check_dir('uploaded_data')
left_column, right_column = st.columns([10, 1])
query_params = st.experimental_get_query_params()

right_column.write("**[Linkedin](https://www.linkedin.com/in/manishsahuiitbhu/)<br>\
                      [:beer:](https://rzp.io/i/K8x2gQ3wG)**",
                   unsafe_allow_html=True)

# options = ['Infection', 'Vaccines']
# what = col1.radio('Type of Data', options)
# area = col2.selectbox("Region", ['test'])

# Specify canvas parameters in application
stroke_width = 2
realtime_update = True 

stroke_color = st.sidebar.color_picker("Stroke color hex: ")
bg_color = st.sidebar.color_picker("Background color hex: ", "#eee")

# drawing_mode = st.sidebar.selectbox(
#     "Drawing tool:", ("rect",)
# )

def load_image(path_image):
    img = np.array(Image.open(path_image).convert('RGB'))
    fig = plt.figure()
    plt.axis('off')
    plt.title('Selected Image')
    plt.imshow(img)
    left_column.pyplot(fig, caption="Selected Image")

st.sidebar.warning('Upload an JPG or PNG Image. For best results.')
st.sidebar.info('PRIVACY POLICY: Images are saved to S3')

img_file = st.sidebar.file_uploader(
    "Please Select to Upload an Image", type=['png', 'jpg', 'jpeg'])

if img_file:
    img = Image.open(img_file) if img_file else None
    shape = np.array(img).shape

    # Create a canvas component
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        background_image=img,
        update_streamlit=realtime_update,
        height=shape[0],
        drawing_mode='rect',
        key="canvas",
    )

    if canvas_result.json_data is not None:
        st.dataframe(pd.json_normalize(canvas_result.json_data["objects"]))

    print(f"canvas_result: {canvas_result.json_data['objects']}")
    pressed = st.sidebar.button('Upload to Cloud')

# if img_file is not None:
#     # print(f'tfile: {tfile.name}')
#     load_image(path_image=img_file)
            
# else:
#     st.sidebar.write('Please select valid option')


st.sidebar.write(" ------ ")
st.write("**:beer: Buy me a [beer](https://rzp.io/i/K8x2gQ3wG)**")
expander = st.expander("This app is developed by Manish Sahu.")
expander.write(
    "Contact me on [Linkedin](https://www.linkedin.com/in/manishsahuiitbhu/)")
expander.write(
    "The source code is on [GitHub](https://github.com/ManishSahu53/political-meme-generator)")