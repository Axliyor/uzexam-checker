# status 100 list ni qirqishda muammo
# 1) code xato
# 2) list ga soya tushgan bo'lishi mumkin
# 3) list qirralari to'liq ajaralib turmagan bo'lishi mumkin
# 4) Katta To'rtburchak qora sohalar xato joylashgan bo'lishi mumkin

# status 101 Javoblar sohasini ajratishda xatolik
# sabablar:
# 1) To'rtburchak qora sohalar xato joylashgan bo'lishi mumkin
# 2) Javoblar sohasida soya bo'lishi mumkin
# 3) List g'ijimlandan bo'lishi mumkin

# status 102 Javoblarni sohasini tekshirishda xatolik
# 1) Javoblar sohasini ajratuvchi to'rtburchalar aniqlanmagan bo'lishi mumkin
# 2) Javoblar sohasida soya bo'lishi mumkin
# 3) List g'ijimlandan bo'lishi mumkin


#############################
# status 200 hamasi to'g'ri #
#############################


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
    # path = "test/test1.png"
    # path = "test/shaxzod.jpg"
    path = "test/test6_err_101.png"
    bookId, questionCount, variant, answer, resultPath, status = check(path)
    print(bookId, questionCount, variant, answer, resultPath, status)


# generateTest()
checkTest()
