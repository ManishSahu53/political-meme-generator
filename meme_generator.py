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


def load_image(path_image):
    img = np.array(Image.open(path_image).convert('RGB'))
    fig = plt.figure()
    plt.axis('off')
    plt.title('Selected Image')
    plt.imshow(img)
    col1.pyplot(fig, caption="Selected Image")


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
MAX_IMAGE = 5

st.title('Political Meme Generator (IPMG)', )
st.subheader('IPMG is best way to create Indian Political Memes. Just for Fun.', )

# Calculating Yesterday date
current_date = datetime.datetime.now().strftime('%Y-%m-%d')
logging.info(f'Processing for Date: {current_date}')

util.check_dir('uploaded_data')
col1, col2, col3, col4, col5 = st.columns([2, 2, 10, 10, 1])
query_params = st.experimental_get_query_params()

path_image = util.list_list('data', ('jpg', 'jpeg', 'png'))
print(f'Number of Image found: {len(path_image)}')

col5.write("**[Linkedin](https://www.linkedin.com/in/manishsahuiitbhu/)<br>\
                      [:beer:](https://rzp.io/i/K8x2gQ3wG)**",
                   unsafe_allow_html=True)

options = ['Infection', 'Vaccines']
# what = col1.radio('Type of Data', options)
# area = col2.selectbox("Region", ['test'])

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
col3.write('----------')
col3.write('Selected Image')
col3.write('----------')
col3.image(img, use_column_width=True)

st.write("**:beer: Buy me a [beer](https://rzp.io/i/K8x2gQ3wG)**")
expander = st.expander("This app is developed by Manish Sahu.")
expander.write(
    "Contact me on [Linkedin](https://www.linkedin.com/in/manishsahuiitbhu/)")
expander.write(
    "The source code is on [GitHub](https://github.com/ManishSahu53/political-meme-generator)")