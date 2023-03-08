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
    paths = [
        "test/test1.png",
        "test/test2.png",
        "test/test3.png",
        "test/shaxzod.jpg",
        "test/jamshidbek1.jpg",
        # "test/jamshidbek2.jpg",
        "test/jamshidbek3.jpg",
        "test/jamshidbek4.jpg",
        "test/jamshidbek5.jpg",
        "test/jamshidbek6.jpg",
        "test/jamshidbek7.jpg",
        "test/jamshidbek8.jpg",
        "test/jamshidbek9.jpg",
        "test/jamshidbek10.jpg",
        "test/azizbek1.jpg",
        "test/azizbek2.jpg",
        "test/azizbek3.jpg",
        "test/azizbek4.jpg",
        "test/azizbek5.jpg",
        "test/azizbek6.jpg",
        # "test/azizbek7.jpg"
    ]
    for x in paths:
        bookId, questionCount, variant, answer, resultPath, status = check(x)
        if status == 200:
            print(x, "->OK")
            # print(bookId, questionCount, variant, answer, resultPath, status)
        else:
            print(x, "-> ERROR")


# generateTest()
checkTest()
