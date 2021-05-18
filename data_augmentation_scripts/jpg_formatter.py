# HEIC to JPG image format batch conversion script for Python 3. Tested on Windows 10.
# You will need to have ImageMagick installed: https://www.imagemagick.org/
# Copy this script over to the location where the images are stored


import os
import subprocess

directory = '.'
rightDirectory = 'Right of Sidewalk'
leftDirectory = 'Left of Sidewalk'
middleDirectory = 'Middle of Sidewalk'
unwantedFormats = ('.png', '.heic', '.jpeg')

for root, dirs, files in os.walk(rightDirectory, topdown=True):
    for filename in files:
        if filename.lower().endswith(unwantedFormats):
            print('Converting %s...' % os.path.join(root, filename))
            subprocess.run(["magick", "%s" % os.path.join(root, filename), "%s" % os.path.join(root,(filename[0:-5] + '.jpg'))])
            os.remove(os.path.join(root, filename))
            continue
for root, dirs, files in os.walk(leftDirectory, topdown=True):
    for filename in files :
        if filename.lower().endswith(unwantedFormats):
            print('Converting %s...' % os.path.join(root, filename))
            subprocess.run(["magick", "%s" % os.path.join(root, filename), "%s" % os.path.join(root,(filename[0:-5] + '.jpg'))])
            os.remove(os.path.join(root, filename))
            continue
for root, dirs, files in os.walk(middleDirectory, topdown=True):
    for filename in files :
        if filename.lower().endswith(unwantedFormats):
            print('Converting %s...' % os.path.join(root, filename))
            subprocess.run(["magick", "%s" % os.path.join(root, filename), "%s" % os.path.join(root,(filename[0:-5] + '.jpg'))])
            os.remove(os.path.join(root, filename))
            continue
