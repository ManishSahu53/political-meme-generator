import io
import os
from os import pathconf_names
import s3fs
from PIL import Image
import streamlit as st
import time
import config


# Create connection object.
# `anon=False` means not anonymous, i.e. it uses access keys to pull data.
fs = s3fs.S3FileSystem(anon=False)

def get_images(conn):
    try:
        sheet_url = os.environ.get('public_gsheets_url')
    except:
        sheet_url = st.secrets["public_gsheets_url"]
    
    rows = conn.run_query(f'SELECT * FROM "{sheet_url}"')

    path_image = []
    # Print results.
    for row in rows:
        path_image.append(row.image_path)
    return path_image

@st.cache(ttl=config.ttl_cache)
def load_image(path_s3):
    # st_time = time.time()
    if 's3://' in path_s3:
        path_s3 = path_s3.split('s3://')[1]
    
    with fs.open(path_s3) as f:
        img = f.read()
    image_stream = io.BytesIO(img)
    img = Image.open(image_stream)
    # end_time = time.time()
    # print(f'Time Taken: {end_time - st_time}')
    return img

def load_image_async(path_s3, index, data):
    data[index] = load_image(path_s3=path_s3)
    return data