from PIL import Image
from io import BytesIO
import numpy as np
import base64

def invert(obrazek):
    im_bytes = base64.b64decode(obrazek)

    im_file = BytesIO(im_bytes)
    img = Image.open(im_file)
    im = np.array(img)

    mask = np.full(im.shape, 255)

    mod_img = mask - im
    mod_img = mod_img.astype(np.uint8)

    pil_img = Image.fromarray(mod_img)
    buff = BytesIO()
    pil_img.save(buff, format="PNG")
    new_image_string = base64.b64encode(buff.getvalue()).decode("utf-8")

    return new_image_string