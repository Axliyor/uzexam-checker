import cv2
from answerFinderLib import answerFinder
from answerFinderLib import checkQR
from sheetGenerator import sheetGenerator1


def generateTest():
    newBookId = "10020"
    filePath = sheetGenerator1(newBookId)
    print(filePath)


def checkTest():
    path = "test/test1.png"
    # path = "template/test1.jpg"
    image, bookId, questionCount, error = checkQR(path)
    print(bookId)
    if error:
        print("QR code error!")
    else:
        correctAnswer = ['D'] * questionCount
        resultPath, variant, answer, error = answerFinder(
            image, questionCount, correctAnswer)
        print(resultPath)
        print('Variant:', variant)
        print('Error:', error)
        if not error:
            print('Answer:', answer)


# generateTest()
checkTest()
