'''
By D. Campion
Generate a json file containing the position of colored shaped in a image.
 - available colors: red, blue, green
 - avaialble shapes: circle, square, rectangle, triangle, pentagon
'''

import detectShapes
import json
import os
import argparse

#set the json
fulljson = []

def createJson(directory,file_json, color, shape, testcontrol):
    #loop over image to process
    for filename in os.listdir(directory):
        if filename.endswith(".jpg"):
            print("Process file: ", os.path.join(directory, filename))
            filepath=os.path.join(directory, filename)
            fulljson.append({"image_path":filepath,"rects":detectShapes.extractShapes(filepath,color,shape,testcontrol)})

    with open(file_json, 'w') as f:
        print("Dump the json: ", file_json)
        json.dump(fulljson, f)

if __name__ == "__main__":
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--directory", required=True,
    	help="path to the images folders")
    ap.add_argument("-j", "--json", required=True,
    	help="json filename")
    ap.add_argument("-c", "--color", required=True,
    	help="color to be detected. Coudl be: red, blue, green")
    ap.add_argument("-s", "--shape", required=False,
    	help="shape to be detected. By default: rectangle. Could be: circle, rectangle, square, pentagon, triangle")
    ap.add_argument("-t", "--test", required=False,
    	help="create additional image to control the ouptput. True or False")

    args, leftovers = ap.parse_known_args()

    directory = args.directory
    file_json = args.json
    color = args.color
    shape = args.shape if args.shape is not None else "rectangle"
    if args.test is not None:
        testcontrol = True if args.test == "True" else False
    else:
        testcontrol = False

    createJson(directory, file_json, color, shape, testcontrol)

    print("json created.")
