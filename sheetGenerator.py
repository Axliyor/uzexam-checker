import cv2
import numpy as np
from PIL import Image
from qrCode import getQR


def sheetGenerator1(bookId):
    small_image = getQR(bookId)
    image = cv2.imread("template/template1.png")
    height, width, channels = small_image.shape
    offset = np.array((60, 130))
    image[offset[0]:offset[0] + height, offset[1]
        :offset[1] + width] = small_image
    pdf = Image.fromarray(image)
    path = 'generated/'+bookId+'.pdf'
    pdf.save(path)
    return path


def printResult(image, randname):
    pdf = Image.fromarray(image)
    path = 'generated/'+str(randname)+'.pdf'
    pdf.save(path)
    return path
