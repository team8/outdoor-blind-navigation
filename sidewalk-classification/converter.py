import PIL
import PIL.Image
import PIL.ExifTags
import cv2
import numpy as np

folder = "image.jpg"

img = PIL.Image.open(folder)

exif = {
        PIL.ExifTags.TAGS[k]: v
        for k, v in img._getexif().items()
        if k in PIL.ExifTags.TAGS
}

img = np.array(img)
if exif['Orientation'] == 3:
    img = cv2.rotate(img, cv2.ROTATE_180)
if exif['Orientation'] == 8:
    img = cv2.rotate(img, cv2.ROTATE_90)
if exif['Orientation'] == 6:
    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

cv2.imshow("img", img)
cv2.waitKey(0)
