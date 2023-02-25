import cv2
import numpy
import numpy as np
from positions import sheet1_line_data
from sheetGenerator import printResult
from random import randrange


def printAnswer1(image, answer, correct):
    blokCorrectCount1 = 0
    result = []
    for x in range(30):
        if len(answer[x]) == 1:
            if correct[x] in answer[x]:
                blokCorrectCount1 += 1
                result.append(True)
            else:
                result.append(False)
        else:
            result.append(False)
    blokCorrectCount2 = 0
    for x in range(30, 60):
        if len(answer[x]) == 1:
            if correct[x] in answer[x]:
                blokCorrectCount2 += 1
                result.append(True)
            else:
                result.append(False)
        else:
            result.append(False)
    blokCorrectCount3 = 0
    for x in range(60, 90):
        if len(answer[x]) == 1:
            if correct[x] in answer[x]:
                blokCorrectCount3 += 1
                result.append(True)
            else:
                result.append(False)
        else:
            result.append(False)
    return printImageAnswer1(image, result, blokCorrectCount1, blokCorrectCount2, blokCorrectCount3)


def printImageAnswer1(image, result, blokCorrectCount1, blokCorrectCount2, blokCorrectCount3):
    # print(blokCorrectCount1, blokCorrectCount2, blokCorrectCount3)
    src = cv2.imread('template/success.png')
    small_ok_image = cv2.resize(src, (25, 25))
    height_ok, width_ok, channels = small_ok_image.shape
    src = cv2.imread('template/error.png')
    small_error_image = cv2.resize(src, (25, 25))
    height_error, width_error, channels = small_error_image.shape
    for index in range(90):
        offset = np.array(
            (sheet1_line_data[4][index][1]-12, sheet1_line_data[4][index][0]+120))
        if result[index]:
            image[offset[0]:offset[0] + height_ok, offset[1]:offset[1] + width_ok] = small_ok_image
        else:
            image[offset[0]:offset[0] + height_error, offset[1]:offset[1] + width_error] = small_error_image
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 0.55
    org = (800, 20)
    color = (200, 0, 0)
    thickness = 1
    image = cv2.putText(image, str(blokCorrectCount1), org,
                        font, fontScale, color, thickness, cv2.LINE_AA)
    org = (840, 20)
    image = cv2.putText(image, '{:0.1f}'.format(
        blokCorrectCount1*1.1)+" Ball", org, font, fontScale, color, thickness, cv2.LINE_AA)
    org = (800, 53)
    image = cv2.putText(image, str(blokCorrectCount2), org,
                        font, fontScale, color, thickness, cv2.LINE_AA)
    org = (840, 53)
    image = cv2.putText(image, '{:0.1f}'.format(
        blokCorrectCount2*3.1)+" Ball", org, font, fontScale, color, thickness, cv2.LINE_AA)
    org = (800, 83)
    image = cv2.putText(image, str(blokCorrectCount3), org,
                        font, fontScale, color, thickness, cv2.LINE_AA)
    org = (840, 83)
    image = cv2.putText(image, '{:0.1f}'.format(
        blokCorrectCount3*2.1)+" Ball", org, font, fontScale, color, thickness, cv2.LINE_AA)
    org = (800, 138)
    image = cv2.putText(image, str(blokCorrectCount1+blokCorrectCount2 +
                        blokCorrectCount3), org, font, fontScale, color, thickness, cv2.LINE_AA)
    org = (840, 138)
    image = cv2.putText(image, '{:0.1f}'.format(blokCorrectCount1*1.1+blokCorrectCount2 *
                        3.1+blokCorrectCount3*2.1)+" Ball", org, font, fontScale, color, thickness, cv2.LINE_AA)
    return printResult(image, randrange(777, 77777))
