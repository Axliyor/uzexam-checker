import cv2
from positions import fix
from positions import sheet1_line_data
from imageCrop import four_point_transform
from imageCrop import getPaper
import datetime
import numpy as np
import qrcode
from pyzbar import pyzbar
font = cv2.FONT_ITALIC

def take(elem):
    return elem[0]
def checkQRcode(image):
    image = image[0:300, 0:400]
    barcodes = pyzbar.decode(image)
    barcodeData = barcodes[0].data.decode("utf-8")
    return int(barcodeData[len(barcodeData)-2:]), barcodeData[:15], barcodeData[15:len(barcodeData)-3] 
def setRounds(image, position, list):
    if position == 0:
        cv2.putText(image, 'A', (list[0] - 10, list[1] + 9), font, 1, (0, 0, 0), 1)
    elif position == 1:
        cv2.putText(image, 'B', (list[0] - 10, list[1] + 10), font, 1, (0, 0, 0), 1)
    elif position == 2:
        cv2.putText(image, 'C', (list[0] - 12, list[1] + 10), font, 1, (0, 0, 0), 1)
    elif position == 3:
        cv2.putText(image, 'D', (list[0] - 10, list[1] + 10), font, 1, (0, 0, 0), 1)
    cv2.circle(image, (list[0], list[1]), 17, (0, 0, 0), 1)
def sheetGenerator(student_id, questions_id, questions_count, lastname, firstname, info):
    if questions_count == 30:
        return sheetGeneratorTemplate1(student_id, questions_id, questions_count, lastname, firstname, info)
def sheetGeneratorTemplate1(student_id, questions_id, questions_count, lastname, firstname, info):
    img = qrcode.make(student_id + questions_id + '|' + str(questions_count))
    img.save('images/qr/' + student_id + questions_id + '.png')
    image = cv2.imread("template1.jpg")
    small_image = cv2.resize(cv2.imread('images/qr/' + student_id + questions_id + '.png'), (280, 280))
    height, width, channels = small_image.shape
    offset = np.array((60, 130))
    image[offset[0]:offset[0] + height, offset[1]:offset[1] + width] = small_image
    # cv2.imshow('template', small_image)
    # cv2.waitKey()
    cv2.putText(image, info, (550, 170), font, 1.5, (0, 0, 200), 3)
    cv2.putText(image, lastname, (1150, 520), font, 1, (0, 0, 0), 2)
    cv2.putText(image, firstname, (1150, 635), font, 1, (0, 0, 0), 2)
    cv2.putText(image, str(datetime.datetime.now().strftime("%x")), (1150, 750), font, 1, (0, 0, 0), 2)
    # cv2.imwrite('images/sheet/' + student_id + questions_id + '.png', image)
    return image
def addAnswerToList(k, list):
    if k == 0:
        list.append('A')
    elif k == 1:
        list.append('B')
    elif k == 2:
        list.append('C')
    elif k == 3:
        list.append('D')
def checkAnswerTemplate1(points):
    answer_list = []
    answer_list.append([[],[],[],[],[],[],[],[],[],[]])
    answer_list.append([[],[],[],[],[],[],[],[],[],[]])
    answer_list.append([[],[],[],[],[],[],[],[],[],[]])
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
def checkTemplate1(image, question_count):
    image = check(image, 1400, 1600)
    image = cv2.resize(image, (1009, 1475))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    points = []
    for c in cnts:
        area = cv2.contourArea(c)
        if area < 100:
            cv2.drawContours(thresh, [c], 0, 0, -1)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=3)
    cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    count = 0
    for c in cnts:
        area = cv2.contourArea(c)
        if area > 500 and area < 1000:
            ((x, y), r) = cv2.minEnclosingCircle(c)
            if (y > 75 and y < 165 and x > 450) or (y > 510 and y < 1400): #(y > 90 and y < 150) or 
                points.append([int(x), int(y)])
                count = count + 1
    points.reverse()
    variant = 0
    if points[0][0] > 540 - fix and points[0][0] < 540 + fix and points[0][1] > 142 - fix and points[0][1] < 142 + fix:
        variant = 1
    if points[0][0] > 673 - fix and points[0][0] < 673 + fix and points[0][1] > 142 - fix and points[0][1] < 142 + fix:
        variant = 2
    elif points[0][0] > 805 - fix and points[0][0] < 805 + fix and points[0][1] > 142 - fix and points[0][1] < 142 + fix:
        variant = 3
    elif points[0][0] > 938 - fix and points[0][0] < 938 + fix and points[0][1] > 142 - fix and points[0][1] < 142 + fix:
        variant = 4
    for i in range(len(points)):
        cv2.circle(image, (points[i][0], points[i][1]), 19, (22, 255, 25), 3)
        # cv2.putText(image, str(i), (points[i][0], points[i][1]), font, 1, (0, 25, 255), 2)
    if count > 0:
        return checkAnswerTemplate1(points), image, variant
    return [], image, variant
def check(image, x, y):
    points = []
    image = cv2.resize(image, (x, y))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        area = cv2.contourArea(c)
        if area < 300:
            cv2.drawContours(thresh, [c], 0, 0, -1)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=3)
    cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    count = 0
    for c in cnts:
        area = cv2.contourArea(c)
        if area > 200 and area < 10000:
            ((x, y), r) = cv2.minEnclosingCircle(c)#(1009, 1475)
            if(y > 50 and y < 1550 and x > 50 and x < 1350):
                points.append([int(x), int(y), int(r)])
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
    pts = np.array([(points[point1][0], points[point1][1]), (points[point2][0], points[point2][1]), (points[point3][0], points[point3][1]), (points[point4][0], points[point4][1])], dtype="float32")
    warped = four_point_transform(image, pts)
    return warped
def answerFinder(question_count, image):
    if question_count == 30:
        answer, image, variant = checkTemplate1(image, question_count)
        return variant, answer, image
    else:
        return variant, [], image
def checkAnswerTest(path):
    try:
        image, error = getPaper(path)
        questions_count, student_id, questions_id = checkQRcode(image)
        variant, answer, image = answerFinder(questions_count, image)
        return error, questions_count, student_id, questions_id, variant, answer, image        
    except:
        return True, 0, '', '', 0, [], cv2.imread(path)