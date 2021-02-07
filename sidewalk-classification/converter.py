import os
import PIL
import PIL.Image
import PIL.ExifTags
import cv2
import numpy as np

folder = "test"

def rotate(img_name):
    img = PIL.Image.open(img_name)

    if img is None:
        return

    exif = {
            PIL.ExifTags.TAGS[k]: v
            for k, v in img._getexif().items()
            if k in PIL.ExifTags.TAGS
    }

    img = img.convert('RGB')
    img = np.array(img)
    if exif['Orientation'] == 3:
        img = cv2.rotate(img, cv2.ROTATE_180)
    if exif['Orientation'] == 8:
        img = cv2.rotate(img, cv2.ROTATE_90)
    if exif['Orientation'] == 6:
        img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imwrite(img_name, img)

for file in os.listdir(folder):
    if file.endswith(".JPG") or file.endswith(".jpg"):
        print(os.path.join(folder, file))
        rotate(os.path.join(folder, file))
