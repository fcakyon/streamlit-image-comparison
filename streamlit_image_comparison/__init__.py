import streamlit.components.v1 as components
from PIL import Image
import base64
import io
import os
import uuid

TEMP_DIR = "temp"

__version__ = "0.0.4"

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
	img1_pillow = Image.open(img1)
	img2_pillow = Image.open(img2)

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
