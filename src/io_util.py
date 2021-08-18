import io
import s3fs
from PIL import Image
import streamlit as st

from src import db_util


# Create connection object.
# `anon=False` means not anonymous, i.e. it uses access keys to pull data.
fs = s3fs.S3FileSystem(anon=False)

def get_images(conn):
    sheet_url = st.secrets["public_gsheets_url"]
    rows = conn.run_query(f'SELECT * FROM "{sheet_url}"')

    path_image = []
    # Print results.
    for row in rows:
        path_image.append(row.image_path)
    return path_image

# @st.cache(ttl=600, allow_output_mutation=True)
def load_image(path_s3):
    if 's3://' in path_s3:
        path_s3 = path_s3.split('s3://')[1]
    
    with fs.open(path_s3) as f:
        img = f.read()
    image_stream = io.BytesIO(img)
    img = Image.open(image_stream)
    return img