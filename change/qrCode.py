import cv2
import qrcode
from pyzbar import pyzbar
from numpy import array


def get_data_in_qr(image):
    image = image[0:300, 0:400]
    barcodes = pyzbar.decode(image)
    barcodeData = barcodes[0].data.decode("utf-8")
    return barcodeData.split(" ")


def getQR(bookId):
    img = qrcode.make("https://t.me/uzexam_bot/" +
                      bookId + "/90").convert('RGB')
    img = array(img)
    small_image = cv2.resize(img, (280, 280))
    return small_image
