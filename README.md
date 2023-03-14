<div align="center">
<h2>
    Streamlit Image Comparison Component
</h2>
</div>

<div align="center">
    <a href="https://badge.fury.io/py/streamlit-image-comparison"><img src="https://badge.fury.io/py/streamlit-image-comparison.svg" alt="pypi version"></a>
    <a href="https://pepy.tech/project/streamlit-image-comparison"><img src="https://pepy.tech/badge/streamlit-image-comparison" alt="total downloads"></a>
    <a href="https://huggingface.co/spaces/fcakyon/streamlit-image-comparison"><img src="https://raw.githubusercontent.com/fcakyon/streamlit-image-comparison/main/resources/hf_spaces_badge.svg" alt="HuggingFace Spaces"></a>
    <a href="https://twitter.com/fcakyon"><img src="https://img.shields.io/badge/twitter-fcakyon_-blue?logo=twitter&style=flat" alt="fcakyon twitter"></a>
</div>

A simple Streamlit Component to compare images with a slider in Streamlit apps using [Knightlab's JuxtaposeJS](https://juxtapose.knightlab.com/). It accepts images in any format and makes it possible to set all parameters of the JS component via Python. Live demo at [Huggingface Spaces](https://huggingface.co/spaces/fcakyon/streamlit-image-comparison)

<p align="center">
<a href='https://huggingface.co/spaces/fcakyon/streamlit-image-comparison' target='_blank'> <img src="https://user-images.githubusercontent.com/34196005/143328163-2976a3b6-91d0-47c5-b872-c92dd6ea404e.gif" width="600"></a>

</p>

## Installation
- Install via pip:

```bash
pip install streamlit
pip install streamlit-image-comparison
```

## Example

```python
# Streamlit Image-Comparison Component Example

import streamlit as st
from streamlit_image_comparison import image_comparison

# set page config
st.set_page_config(page_title="Image-Comparison Example", layout="centered")

# render image-comparison
image_comparison(
    img1="image1.jpg",
    img2="image2.jpg",
)
```

## Supported Image Formats

```python

# image path
image = "image.jpg"

# image url
image = "https://some-url.com/image.jpg"

# pil image
from PIL import Image
image = Image.open("image.jpg")

# opencv image
import cv2
image = cv2.cvtColor(cv2.imread("image.jpg"), cv2.COLOR_BGR2RGB)

# render image-comparison
image_comparison(
    img1=image,
    img2=image,
)
```

## Customization

```python
image_comparison(
    img1="image1.jpg",
    img2="image2.jpg",
    label1="text1",
    label2="text1",
    width=700,
    starting_position=50,
    show_labels=True,
    make_responsive=True,
    in_memory=True,
)
```

## Improvements

What is the difference between this repo and [robmarkcole's](https://github.com/robmarkcole/streamlit-image-juxtapose)?

- This is a pypi installable package
- This does not require the images to be saved under `site-packages/streamlit/static/`
- This accepts any type of image as input (doesn't have to be present in local)
- This can utilize all parameters of the JS component

## References
- https://juxtapose.knightlab.com/
- https://github.com/robmarkcole/streamlit-image-juxtapose
