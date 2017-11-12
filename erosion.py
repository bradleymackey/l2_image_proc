import cv2
import sys
import numpy as np

def fixIndexValue(index,maxIndex):
    """fixes an index value to mimic the reflection off the border property, so we do not get an out-of-bounds error when the structuring element is in the corner"""
    if index < 0:
        # if we are trying to access an index less than 0, just invert the index (reflected value)
        return -index
    elif index>=maxIndex:
        # if we are trying to access a number greater than the max, return the reflected value
        return maxIndex-(index-maxIndex)-1
    else:
        # otherwise, just return the value
        return index

def pixelValuesForStruturingElementPosition(image,horizontal,vertical):
    """returns the pixel values that the 5x5 structuring element is currently over for a given image and centre position where the strucuring element currently is"""
    # where the values will be stored
    values = []
    # get image size using numpy
    height, width = np.shape(image)
    # iterate over all neighbours of this pixel to find the minimum
    # k is the current neighbouring pixel horizontal index
    for structuringHorizontal in range(horizontal-2,horizontal+3):
        # l is the current neighbouring pixel vertical index
        for structuringVertical in range(vertical-2,vertical+3):
            # fix the index values so we don't get an out-of-bounds error
            structuringHorizontal = fixIndexValue(structuringHorizontal,width)
            structuringVertical = fixIndexValue(structuringVertical,height)
            # get the pixel value of this neighbouring pixel
            neighbourPixel = image[structuringHorizontal][structuringVertical]
            values.append(neighbourPixel)
    # return the pixel values that the structuring element is currently over
    return values

def morphologicalTransformation(image,selectionFunction):
    """performs a morphological transformation on a given image using a given selection function (e.g. max, min) which selects a given pixel from the pixels that the structuring element is currently over"""
    # define the structuring element
    structure = np.ones((5,5),np.uint8)
    # get image size using numpy
    height, width = np.shape(image)
    # make a copy of the image to save our resultant image to
    result_image = image.copy()
    # iterate over all pixels in the image
    # current horizontal index
    for horizontal in range(0,width):
        # current vertical index
        for vertical in range(0,height):
            # the the current pixel values that the structuring element is currently over
            structuringElementPixels = pixelValuesForStruturingElementPosition(image,horizontal,vertical)
            # set the value at this location to be a chosen pixel according to the `selectionFunction`
            result_image[horizontal][vertical] = selectionFunction(structuringElementPixels)
    # return the resultant image
    return result_image

def imageErosion(image):
    """performs erosion on an image and returns this"""
    # produce the eroded image by using the 'min' selection function which will use the minimum pixel value that the structuring element is currently over
    eroded_image = morphologicalTransformation(image,min)
    # return the eroded image
    return eroded_image

# read the image from the filename in greyscale
greyscale_image = cv2.imread(sys.argv[1],0)
# obtain the eroded image
eroded_image = imageErosion(greyscale_image)
# save the eroded image back to disk, with the user-specified filename
cv2.imwrite(sys.argv[2],eroded_image)
