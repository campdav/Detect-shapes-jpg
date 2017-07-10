# import the necessary packages
from lib.shapeDetector import ShapeDetector
from lib.colorLabeler import ColorLabeler
import argparse
import imutils
import cv2
import json

file_json = "./data/output/train.json"
fulljson = []
rects = []


def extractShapes(imagePath,target_color="red", target_shape="rectangle", testcontrol=False):
    rects = []
    # load the image and resize it to a smaller factor so that
    # the shapes can be approximated better
    image = cv2.imread(imagePath)
    resized = imutils.resize(image, width=1000)
    #resized = image
    ratio = image.shape[0] / float(resized.shape[0])

    # blur the resized image slightly, then convert it to both
    # grayscale and the L*a*b* color spaces
    #blurred = cv2.GaussianBlur(resized, (5, 5), 0)
    blurred = resized

    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)

    lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)

    thresh = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)[1]

    if testcontrol ==True:
        cv2.imwrite("./Data/output/resized.jpg", resized)
        cv2.imwrite("./Data/output/blurred.jpg", blurred)
        cv2.imwrite("./Data/output/gray.jpg", gray)
        cv2.imwrite("./Data/output/lab.jpg", lab)
        cv2.imwrite("./Data/output/thresh.jpg", thresh)

    # find contours in the thresholded image
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
    	cv2.CHAIN_APPROX_SIMPLE)

    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    # initialize the shape detector and color labeler
    sd = ShapeDetector()
    cl = ColorLabeler()

    # loop over the contours
    for c in cnts:
        # compute the center of the contour, then detect the name of the
        # shape using only the contour
        M = cv2.moments(c)

        if M["m00"] > 0:
            cX = int((M["m10"] / M["m00"]) * ratio)
            cY = int((M["m01"] / M["m00"]) * ratio)

    		# detect the shape of the contour and label the color
            shape = sd.detect(c)
            color = cl.label(lab, c)

            if (color, shape)==(target_color,target_shape):
        		# multiply the contour (x, y)-coordinates by the resize ratio,
        		# then draw the contours and the name of the shape and labeled
        		# color on the image
                c = c.astype("float")
                c *= ratio
                c = c.astype("int")

                #retrieve corners
                x1, y1, w, h = cv2.boundingRect(c)
                x2, y2 = x1 + w, y1 + h
                #print(x1, y1, w, h)

                rect = {"x1":x1,"x2":x2,"y1":y1,"y2":y2}
                rects.append(rect)
                #print(rects)

                text = "{} {}".format(color, shape)
                cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
                cv2.putText(image, text, (cX, cY),
        			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    if testcontrol == True:
        cv2.imwrite("./Data/output/output.jpg", image)

    return rects

if __name__ == "__main__":
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True,
    	help="path to the input image")
    ap.add_argument("-c", "--color", required=True,
    	help="color of the shape to be detected")
    ap.add_argument("-s", "--shape", required=True,
    	help="shape to be detected")
    args = vars(ap.parse_args())
    result = extractShapes(args["image"],args["color"], args["shape"], testcontrol=True)

    if result:
        print("[*] Succces extract %s %s from %s: %s" % (args["color"], args["shape"], args["image"], result))


"""
===========================================
Running Test:
  python detect_Shapes.py --image zz.pdf --color red --shape rectangle
  [*] Succces extract red rectangle from zz.pdf

===========================================
"""
