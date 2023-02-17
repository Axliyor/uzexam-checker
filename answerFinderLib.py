import cv2
import numpy as np
from imageCrop import getPaper
from imageCrop import four_point_transform
from math import sqrt
from math import fabs
from positions import sheet1_line_data
fix = 10
differenceFix = 20
def template(image, question_count):
    if question_count == 90:
        answer, variant, error = checkTemplate1(image)
        return variant, answer, error 
    else:
        return variant, [], False
def answerFinder(path, questionCount):
    try:
        image, error1 = getPaper(path)
        variant, answer, error2 = template(image, questionCount)
        return variant, answer, error1 or error2
    except:
        return 0, [], True
def checkTemplate1(image):
    image, variant, error = cropPaper(image)
    if error:
        return [], variant, error
    image = cv2.resize(image, (959, 1400))
    image, error = cropAnswerTemp1(image)
    if error:
        return [], variant, error
    # cv2.imwrite('service/templates/test.png', image)  
    image = cv2.resize(image, (795, 809))
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
        if area > 250 and area < 370:
            ((x, y), r) = cv2.minEnclosingCircle(c) 
            points.append([int(x), int(y)])
            count = count + 1
    points.reverse()
    for i in range(len(points)):
        cv2.circle(image, (points[i][0]-3, points[i][1]-1), 11, (22, 255, 25), 1)
        
    # cv2.imshow('template', image)
    # cv2.waitKey()
    if count > 0:
        return checkAnswerTemplate1(points), variant, False
    return [], variant, True
def cropAnswerTemp1(image):
    points = []
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
        if area > 600 and area < 900:
            ((x, y), r) = cv2.minEnclosingCircle(c) 
            if(y > 500 and y < 1350 and x > 20 and x < 950):
                points.append([int(x), int(y), int(r), area])
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
    length1 = sqrt((points[point1][0] - points[point3][0])**2+(points[point1][1] - points[point3][1])**2)
    length2 = sqrt((points[point2][0] - points[point4][0])**2+(points[point2][1] - points[point4][1])**2)
    difference = fabs(length1-length2)
    pts = np.array([(points[point1][0]+20, points[point1][1]-20), (points[point2][0]-20, points[point2][1]-20), (points[point3][0]-20, points[point3][1]+20), (points[point4][0]+20, points[point4][1]+20)], dtype="float32")
    warped = four_point_transform(image, pts)
    return warped, difference > differenceFix

def cropPaper(image):
    points = []
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
        if area > 1000 and area < 2000:
            ((x, y), r) = cv2.minEnclosingCircle(c)
            if(y > 50 and y < 1550 and x > 50 and x < 1350):
                points.append([int(x), int(y), int(r), area])
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
    length1 = sqrt((points[point1][0] - points[point3][0])**2+(points[point1][1] - points[point3][1])**2)
    length2 = sqrt((points[point2][0] - points[point4][0])**2+(points[point2][1] - points[point4][1])**2)
    difference = fabs(length1-length2)
    variantCount = 0
    variantPath = [0,0]
    for x in points:
        if x[1] > 150 and x[1] < 250 and x[0] > 700:
            variantPath[0] = x[0]
            variantPath[1] = x[1]
            variantCount+=1
    variant = 0
    if variantCount > 1:
        variant = 0
    else:
        for index in range(4):
            if(variantPath[0] > sheet1_line_data[3][index] - fix and variantPath[0] < sheet1_line_data[3][index] + fix):
                variant = index + 1
                break
    pts = np.array([(points[point1][0], points[point1][1]), (points[point2][0], points[point2][1]), (points[point3][0], points[point3][1]), (points[point4][0], points[point4][1])], dtype="float32")
    warped = four_point_transform(image, pts)
    return warped, variant, difference > differenceFix
def checkAnswerTemplate1(points):
    answer_list = []
        
    answer_list.append([[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]])
    answer_list.append([[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]])
    answer_list.append([[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]])
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