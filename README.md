# streamlit-image-comparison

A simple Streamlit Component to compare images with a slider in Streamlit apps using [Knightlab's JuxtaposeJS](https://juxtapose.knightlab.com/). It accepts images in any format and makes it possible to set all parameters of the JS component via Python. Try it on [...](...)

<p align="center">
<img src="https://user-images.githubusercontent.com/34196005/143328163-2976a3b6-91d0-47c5-b872-c92dd6ea404e.gif" width="600">
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

## References
- https://juxtapose.knightlab.com/
- https://github.com/robmarkcole/streamlit-image-juxtapose
