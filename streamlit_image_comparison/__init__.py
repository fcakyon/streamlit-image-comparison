import streamlit.components.v1 as components
from PIL import Image
import base64
import io
import os
import uuid
from typing import Union
import requests
import numpy as np

TEMP_DIR = "temp"

__version__ = "0.0.4"

def exif_transpose(image: Image.Image):
	"""
	Transpose a PIL image accordingly if it has an EXIF Orientation tag.
	Inplace version of https://github.com/python-pillow/Pillow/blob/master/src/PIL/ImageOps.py exif_transpose()
	:param image: The image to transpose.
	:return: An image.
	"""
	exif = image.getexif()
	orientation = exif.get(0x0112, 1)  # default 1
	if orientation > 1:
		method = {
			2: Image.FLIP_LEFT_RIGHT,
			3: Image.ROTATE_180,
			4: Image.FLIP_TOP_BOTTOM,
			5: Image.TRANSPOSE,
			6: Image.ROTATE_270,
			7: Image.TRANSVERSE,
			8: Image.ROTATE_90,
		}.get(orientation)
		if method is not None:
			image = image.transpose(method)
			del exif[0x0112]
			image.info["exif"] = exif.tobytes()
	return image

def read_image_as_pil(image: Union[Image.Image, str, np.ndarray], exif_fix: bool = False):
	"""
	Loads an image as PIL.Image.Image.
	Args:
		image : Can be image path or url (str), numpy image (np.ndarray) or PIL.Image
	"""
	# https://stackoverflow.com/questions/56174099/how-to-load-images-larger-than-max-image-pixels-with-pil
	Image.MAX_IMAGE_PIXELS = None

	if isinstance(image, Image.Image):
		image_pil = image.convert('RGB')
	elif isinstance(image, str):
		# read image if str image path is provided
		try:
			image_pil = Image.open(
				requests.get(image, stream=True).raw if str(image).startswith("http") else image
			).convert("RGB")
			if exif_fix:
				image_pil = exif_transpose(image_pil)
		except:  # handle large/tiff image reading
			try:
				import skimage.io
			except ImportError:
				raise ImportError("Please run 'pip install -U scikit-image imagecodecs' for large image handling.")
			image_sk = skimage.io.imread(image).astype(np.uint8)
			if len(image_sk.shape) == 2:  # b&w
				image_pil = Image.fromarray(image_sk, mode="1").convert("RGB")
			elif image_sk.shape[2] == 4:  # rgba
				image_pil = Image.fromarray(image_sk, mode="RGBA").convert("RGB")
			elif image_sk.shape[2] == 3:  # rgb
				image_pil = Image.fromarray(image_sk, mode="RGB")
			else:
				raise TypeError(f"image with shape: {image_sk.shape[3]} is not supported.")
	elif isinstance(image, np.ndarray):
		if image.shape[0] < 5:  # image in CHW
			image = image[:, :, ::-1]
		image_pil = Image.fromarray(image).convert("RGB")
	else:
		raise TypeError("read image with 'pillow' using 'Image.open()'")

	return image_pil

def pillow_to_base64(image: Image.Image) -> str:
	"""
	Convert a PIL image to a base64-encoded string.

	Parameters
	----------
	image: PIL.Image.Image
		The image to be converted.

	Returns
	-------
	str
		The base64-encoded string.
	"""
	in_mem_file = io.BytesIO()
	image.save(in_mem_file, format="JPEG", subsampling=0, quality=100)
	img_bytes = in_mem_file.getvalue()  # bytes
	image_str = base64.b64encode(img_bytes).decode("utf-8")
	base64_src = f"data:image/jpg;base64,{image_str}"
	return base64_src

def local_file_to_base64(image_path: str) -> str:
	"""
	Convert a local image file to a base64-encoded string.

	Parameters
	----------
	image_path: str
		The path to the image file.

	Returns
	-------
	str
		The base64-encoded string.
	"""
	file_ = open(image_path, "rb")
	img_bytes = file_.read()
	image_str = base64.b64encode(img_bytes).decode("utf-8")
	file_.close()
	base64_src = f"data:image/jpg;base64,{image_str}"
	return base64_src

def pillow_local_file_to_base64(image: Image.Image, temp_dir: str):
	"""
	Convert a Pillow image to a base64 string, using a temporary file on disk.

	Parameters
	----------
	image : PIL.Image.Image
		The Pillow image to convert.
	temp_dir : str
		The directory to use for the temporary file.

	Returns
	-------
	str
		A base64-encoded string representing the image.
	"""
	# Create temporary file path using os.path.join()
	img_path = os.path.join(temp_dir, str(uuid.uuid4()) + ".jpg")

	# Save image to temporary file
	image.save(img_path, subsampling=0, quality=100)

	# Convert temporary file to base64 string
	base64_src = local_file_to_base64(img_path)

	return base64_src

def image_comparison(
	img1: str,
	img2: str,
	label1: str = "1",
	label2: str = "2",
	width: int = 704,
	show_labels: bool = True,
	starting_position: int = 50,
	make_responsive: bool = True,
	in_memory: bool = False,
) -> components.html:
	"""
	Create a comparison slider for two images.
	
	Parameters
	----------
	img1: str
		Path to the first image.
	img2: str
		Path to the second image.
	label1: str, optional
		Label for the first image. Default is "1".
	label2: str, optional
		Label for the second image. Default is "2".
	width: int, optional
		Width of the component in pixels. Default is 704.
	show_labels: bool, optional
		Whether to show labels on the images. Default is True.
	starting_position: int, optional
		Starting position of the slider as a percentage (0-100). Default is 50.
	make_responsive: bool, optional
		Whether to enable responsive mode. Default is True.
	in_memory: bool, optional
		Whether to handle pillow to base64 conversion in memory without saving to local. Default is False.

	Returns
	-------
	components.html
		Returns a static component with a timeline
	"""
	# Prepare images
	img1_pillow = read_image_as_pil(img1)
	img2_pillow = read_image_as_pil(img2)

	img_width, img_height = img1_pillow.size
	h_to_w = img_height / img_width
	height = int((width * h_to_w) * 0.95)

	if in_memory:
		# Convert images to base64 strings
		img1 = pillow_to_base64(img1_pillow)
		img2 = pillow_to_base64(img2_pillow)
	else:
		# Create base64 strings from temporary files
		os.makedirs(TEMP_DIR, exist_ok=True)
		for file_ in os.listdir(TEMP_DIR):
			if file_.endswith(".jpg"):
				os.remove(os.path.join(TEMP_DIR, file_))
		img1 = pillow_local_file_to_base64(img1_pillow, TEMP_DIR)
		img2 = pillow_local_file_to_base64(img2_pillow, TEMP_DIR)

	# Load CSS and JS
	cdn_path = "https://cdn.knightlab.com/libs/juxtapose/latest"
	css_block = f'<link rel="stylesheet" href="{cdn_path}/css/juxtapose.css">'
	js_block = f'<script src="{cdn_path}/js/juxtapose.min.js"></script>'

	# write html block
	htmlcode = f"""
		<style>body {{ margin: unset; }}</style>
		{css_block}
		{js_block}
		<div id="foo" style="height: {height}; width: {width or '100%'};"></div>
		<script>
		slider = new juxtapose.JXSlider('#foo',
			[
				{{
					src: '{img1}',
					label: '{label1}',
				}},
				{{
					src: '{img2}',
					label: '{label2}',
				}}
			],
			{{
				animate: true,
				showLabels: {'true' if show_labels else 'false'},
				showCredits: true,
				startingPosition: "{starting_position}%",
				makeResponsive: {'true' if make_responsive else 'false'},
			}});
		</script>
		"""
	static_component = components.html(htmlcode, height=height, width=width)

	return static_component
