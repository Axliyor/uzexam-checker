import cv2
from answerFinderLib import answerFinder
from answerFinderLib import check
from answerFinderLib import checkQR
from sheetGenerator import sheetGenerator1


def generateTest():
    newBookId = "10020"
    filePath = sheetGenerator1(newBookId)
    print(filePath)


def checkTest():
    path = "test/pressed.jpg"
    # path = "template/test1.jpg"
    check(path)

# generateTest()
# checkTest()
# bookId = "34354sdfsdf"
# text = "https://t.me/uzexam_bot/" + bookId + "/90"
# print(text.split('/')[4],text.split('/')[5])
