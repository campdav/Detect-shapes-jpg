# Detect-shapes-jpg
Detect colored shapes in a directory of images and create a json describing detected shapes.

**detectShapes.py** adapted from http://www.pyimagesearch.com/2016/02/08/opencv-shape-detection/

The first objective is to detect **rectangles** (but it work also for other shapes), the json file is shaped as input for [TensorBox](https://github.com/TensorBox/TensorBox/) project.

Note: background of images have to be dark/black.

## prerequisites:
 - cv2
 - imutils


## createjson.py

python createjson.py -d ./data/tagged -j ./data/output/file.json -c [red, blue, green] -s [rectangle, triangle, square, circle pentagon] -t [True,False]

 - **d**: path to the images folders
 - **j**: json filename
 - **c**: color to be detected. could be: red, blue, green
 - **s**: (optional) shape to be detected. By default: rectangle. Could be: circle, rectangle, square, pentagon, triangle")
 - **t**: (optional) create additional image to control the output. True or False

## detectShapes.py

**detectShapes.py** can be used alone:

python detectShapes.py --image zz.pdf --color [red, blue, green] --shape [rectangle, square, triangle, circle, pentangon]
