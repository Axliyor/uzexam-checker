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
from answerFinderLib import checkQR
from sheetGenerator import sheetGenerator1


def generateTest():
    newBookId = "10020"
    filePath = sheetGenerator1(newBookId)
    print(filePath)


def checkTest():
    # paths = [
    #     "test/test1.png",
    #     "test/test2.png",
    #     "test/test3.png",
    #     "test/shaxzod.jpg",
    #     "test/jamshidbek1.jpg",
    #     # "test/jamshidbek2.jpg",
    #     "test/jamshidbek3.jpg",
    #     "test/jamshidbek4.jpg",
    #     "test/jamshidbek5.jpg",
    #     "test/jamshidbek6.jpg",
    #     "test/jamshidbek7.jpg",
    #     "test/jamshidbek8.jpg",
    #     "test/jamshidbek9.jpg",
    #     "test/jamshidbek10.jpg",
    #     "test/azizbek1.jpg",
    #     "test/azizbek2.jpg",
    #     "test/azizbek3.jpg",
    #     "test/azizbek4.jpg",
    #     "test/azizbek5.jpg",
    #     "test/azizbek6.jpg",
    #     # "test/azizbek7.jpg"
    # ]
    # for x in paths:
    img = cv2.imread("test/shaxzod.jpg")
    for whitespace in range(1, 6):
        for retry in range(4):
            image, bookId, questionCount, error, status = checkQR(img, retry, whitespace)
            if error:
                if (retry == 3 and whitespace == 5):
                    print("error: ",100)
                    return
                    # return bookId, questionCount, 0, [], "", 100
            else:
                # javoblarni service ga berish
                correctAnswer = ['A'] * questionCount
                resultPath, variant, answer, error, status = answerFinder(
                    image, questionCount, correctAnswer)
                if status == 101 and retry == 3 and whitespace == 5:
                    print("error: ",101)
                    return
                if not error:
                    print("natija: ",bookId, questionCount, variant, answer, resultPath, 200)
                    return
                elif retry == 3 and whitespace == 5:
                    print(102)
                    return
                    


# generateTest()
checkTest()
