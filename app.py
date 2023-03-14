import streamlit as st

from streamlit_image_comparison import exif_transpose
from streamlit_image_comparison import read_image_as_pil
from streamlit_image_comparison import pillow_to_base64
from streamlit_image_comparison import local_file_to_base64
from streamlit_image_comparison import local_file_to_base64
from streamlit_image_comparison import pillow_local_file_to_base64
from streamlit_image_comparison import image_comparison

IMAGE_TO_URL = {
    "sample_image_1": "https://user-images.githubusercontent.com/34196005/143309873-c0c1f31c-c42e-4a36-834e-da0a2336bb19.jpg",
    "sample_image_2": "https://user-images.githubusercontent.com/34196005/143309867-42841f5a-9181-4d22-b570-65f90f2da231.jpg",
}


st.set_page_config(
    page_title="Streamlit Image Comparison",
    page_icon="🔥",
    layout="centered",
    initial_sidebar_state="auto",
)

st.markdown(
    """
    <h2 style='text-align: center'>
    Streamlit Image Comparison Demo
    </h2>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    """
    <p style='text-align: center'>
    <br />
    Follow me for more! <a href='https://twitter.com/fcakyon' target='_blank'> <img src="https://img.icons8.com/color/48/000000/twitter--v1.png" height="30"></a><a href='https://github.com/fcakyon' target='_blank'><img src="https://img.icons8.com/fluency/48/000000/github.png" height="27"></a><a href='https://www.linkedin.com/in/fcakyon/' target='_blank'><img src="https://img.icons8.com/fluency/48/000000/linkedin.png" height="30"></a> <a href='https://fcakyon.medium.com/' target='_blank'><img src="https://img.icons8.com/ios-filled/48/000000/medium-monogram.png" height="26"></a>
    </p>
    """,
    unsafe_allow_html=True,
)

st.write("##")

with st.form(key="Streamlit Image Comparison"):
    # image one inputs
    col1, col2 = st.columns([3, 1])
    with col1:
        img1_url = st.text_input("Image one URL:", value=IMAGE_TO_URL["sample_image_1"])
    with col2:
        img1_text = st.text_input("Image one text:", value="YOLOX")

    # image two inputs
    col1, col2 = st.columns([3, 1])
    with col1:
        img2_url = st.text_input("Image two URL:", value=IMAGE_TO_URL["sample_image_2"])
    with col2:
        img2_text = st.text_input("Image two text:", value="SAHI+YOLOX")

    # continious parameters
    col1, col2 = st.columns([1, 1])
    with col1:
        starting_position = st.slider(
            "Starting position of the slider:", min_value=0, max_value=100, value=50
        )
    with col2:
        width = st.slider(
            "Component width:", min_value=400, max_value=1000, value=700, step=100
        )

    # boolean parameters
    col1, col2, col3, col4 = st.columns([1, 3, 3, 3])
    with col2:
        show_labels = st.checkbox("Show labels", value=True)
    with col3:
        make_responsive = st.checkbox("Make responsive", value=True)
    with col4:
        in_memory = st.checkbox("In memory", value=True)

    # centered submit button
    col1, col2, col3 = st.columns([6, 4, 6])
    with col2:
        submit = st.form_submit_button("Update Render 🔥")

static_component = image_comparison(
    img1=img1_url,
    img2=img2_url,
    label1=img1_text,
    label2=img2_text,
    width=width,
    starting_position=starting_position,
    show_labels=show_labels,
    make_responsive=make_responsive,
    in_memory=in_memory,
)
