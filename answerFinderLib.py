import cv2
import numpy as np
from qrCode import get_data_in_qr
from imageCrop import getPaper
from imageCrop import four_point_transform
from math import sqrt
from math import fabs
from positions import sheet1_line_data
from printAnswerLib import printAnswer1
fix = 10
differenceFix = 20


def check(path):
    img = cv2.imread(path)
    # retry listni ajratish uchun tasvir ichiki tekshiruvi soni
    for whitespace in range(1, 6):
        for retry in range(4):
            image, bookId, questionCount, error, status = checkQR(img, retry, whitespace)
            if error:
                if (retry == 3 and whitespace == 5):
                    return bookId, questionCount, 0, [], "", 100
            else:
                correctAnswer = ['A'] * questionCount
                resultPath, variant, answer, error, status = answerFinder(
                    image, questionCount, correctAnswer)
                if status == 101 and retry == 3 and whitespace == 5:
                    return bookId, questionCount, 0, [], "", 101
                if not error:
                    return bookId, questionCount, variant, answer, resultPath, 200
                elif retry == 3 and whitespace == 5:
                    return bookId, questionCount, 0, [], "", 102


def checkQR(img, retry, whitespace):
    try:
        image = img
        error = False
        thresh = 200
        if (retry == 0):
            image, error = getPaper(img, [thresh, thresh], whitespace)
        elif (retry == 1):
            image1, error = getPaper(img, [thresh, thresh], whitespace)
            image, error = getPaper(image1, [thresh, thresh], whitespace)
        elif (retry == 2):
            image1, error = getPaper(img, [thresh, thresh], whitespace)
            image2, error = getPaper(image1, [thresh, thresh], whitespace)
            image, error = getPaper(image2, [thresh, thresh], whitespace)
        elif (retry == 3):
            image1, error = getPaper(img, [thresh, thresh], whitespace)
            image2, error = getPaper(image1, [thresh, thresh], whitespace)
            image3, error = getPaper(image2, [thresh, thresh], whitespace)
            image, error = getPaper(image3, [thresh, thresh], whitespace)
        qrcode = get_data_in_qr(image)
        # https://t.me/uzexam_bot/2938/90
        return image, qrcode[4], int(qrcode[5]), False, 0
    except:
        return 0, "0", 0, True, 100


def template(image, question_count, correctAnswer):
    if question_count == 90:
        img, answer, variant, error = checkTemplate1(image)
        if not error:
            resultPath = printAnswer1(img, answer, correctAnswer)
            return resultPath, variant, answer, error
        else:
            return "", variant, [], True
    else:
        return "", variant, [], True


def answerFinder(image3, questionCount, correctAnswer):
    try:
        resultPath, variant, answer, error = template(
            image3, questionCount, correctAnswer)
        return resultPath, variant, answer, error, 0
    except:
        return "", 0, [], True, 101


def checkTemplate1(image):

    image = cv2.resize(image, (1200, 1600))
    image, variant, error = cropPaperTemp1(image)

    if error:
        return [], variant, error

    image = cv2.resize(image, (959, 1400))
    img = image
    image, error = cropAnswerTemp1(image)
    if error:
        return [], variant, error
    image = cv2.resize(image, (795, 809))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    points = []
    for c in cnts:
        area = cv2.contourArea(c)
        if area < 100:
            cv2.drawContours(thresh, [c], 0, 0, -1)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=3)
    cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    count = 0
    for c in cnts:
        area = cv2.contourArea(c)
        if area > 250 and area < 420:
            ((x, y), r) = cv2.minEnclosingCircle(c)
            points.append([int(x), int(y)])
            count = count + 1
    points.reverse()
    variant = 0
    # for i in range(len(points)):
    #     cv2.circle(image, (points[i][0]-3, points[i][1]-1), 11, (22, 255, 25), 1)
    return img, checkAnswerTemplate1(points), variant, False


def cropAnswerTemp1(image):
    points = []
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        area = cv2.contourArea(c)
        if area < 300:
            cv2.drawContours(thresh, [c], 0, 0, -1)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=3)
    cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    count = 0
    for c in cnts:
        area = cv2.contourArea(c)
        if area > 600 and area < 900:
            ((x, y), r) = cv2.minEnclosingCircle(c)
            if (y > 500 and y < 1350 and x > 20 and x < 950):
                points.append([int(x), int(y)])
                count = count + 1
    points.reverse()
    maps = points[0:2]
    maps.sort(key=take)
    points[0:2] = maps
    maps = points[count - 2:count]
    maps.sort(key=take)
    points[count - 2:count] = maps
    point1 = 0
    point2 = 1
    point3 = count - 1
    point4 = count - 2
    length1 = sqrt((points[point1][0] - points[point3][0])
                   ** 2+(points[point1][1] - points[point3][1])**2)
    length2 = sqrt((points[point2][0] - points[point4][0])
                   ** 2+(points[point2][1] - points[point4][1])**2)
    difference = fabs(length1-length2)
    pts = np.array([(points[point1][0]+20, points[point1][1]-20), (points[point2][0]-20, points[point2][1]-20),
                   (points[point3][0]-20, points[point3][1]+20), (points[point4][0]+20, points[point4][1]+20)], dtype="float32")
    warped = four_point_transform(image, pts)
    return warped, difference > differenceFix


def cropPaperTemp1(image):
    points = []

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        area = cv2.contourArea(c)
        if area < 300:
            cv2.drawContours(thresh, [c], 0, 0, -1)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=3)

    cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    count = 0
    variants = []
    for c in cnts:
        area = cv2.contourArea(c)
        if (area < 1200 and area > 500):
            ((x, y), r) = cv2.minEnclosingCircle(c)
            if (y > 150 and y < 250 and x > 500):
                variants.append([int(x), int(y)])
        elif area > 1000 and area < 2000:
            ((x, y), r) = cv2.minEnclosingCircle(c)
            if ((((y > 10 and y < 100) or (y > 1450 and y < 1585)) and x > 20 and x < 1350)):
                points.append([int(x), int(y)])
                count = count + 1
    points.reverse()
    maps = points[0:2]
    maps.sort(key=take)
    points[0:2] = maps
    maps = points[count - 2:count]
    maps.sort(key=take)
    points[count - 2:count] = maps
    point1 = 0
    point2 = 1
    point3 = count - 1
    point4 = count - 2
    length1 = sqrt((points[point1][0] - points[point3][0])
                   ** 2+(points[point1][1] - points[point3][1])**2)
    length2 = sqrt((points[point2][0] - points[point4][0])
                   ** 2+(points[point2][1] - points[point4][1])**2)
    difference = fabs(length1-length2)
    variant = 0

    # variantCount = 0
    # variantPath = [0, 0]
    # for x in variants:
    #     if x[1] > 150 and x[1] < 250 and x[0] > 500:
    #         variantPath[0] = x[0]
    #         variantPath[1] = x[1]
    #         variantCount += 1
    #
    # if variantCount > 1:
    #     variant = 0
    # else:
    #     for index in range(4):
    #         if (variantPath[0] > sheet1_line_data[3][index] - 80 and variantPath[0] < sheet1_line_data[3][index] + 80):
    #             variant = index + 1
    #             break
    pts = np.array([(points[point1][0], points[point1][1]), (points[point2][0], points[point2][1]),
                   (points[point3][0], points[point3][1]), (points[point4][0], points[point4][1])], dtype="float32")
    warped = four_point_transform(image, pts)

    return warped, variant, difference > differenceFix


def checkAnswerTemplate1(points):
    answer_list = []
    answer_list.append([[], [], [], [], [], [], [], [], [], [], [], [], [], [], [
    ], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []])
    answer_list.append([[], [], [], [], [], [], [], [], [], [], [], [], [], [], [
    ], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []])
    answer_list.append([[], [], [], [], [], [], [], [], [], [], [], [], [], [], [
    ], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []])
    for m in range(3):
        for k in range(4):
            for i in range(len(sheet1_line_data[m][k])):
                for j in range(len(points)):
                    if sheet1_line_data[m][k][i][0] - fix < points[j][0] and sheet1_line_data[m][k][i][0] + fix > points[j][0] and sheet1_line_data[m][k][i][1] - fix < points[j][1] and sheet1_line_data[m][k][i][1] + fix > points[j][1]:
                        addAnswerToList(k, answer_list[m][i])
                        break
    answer = []
    for j in range(3):
        for i in range(len(answer_list[j])):
            answer.append(answer_list[j][i])
    return answer


def take(elem):
    return elem[0]


def addAnswerToList(k, list):
    if k == 0:
        list.append('A')
    elif k == 1:
        list.append('B')
    elif k == 2:
        list.append('C')
    elif k == 3:
        list.append('D')
