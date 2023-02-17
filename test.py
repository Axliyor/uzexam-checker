import cv2
from answerFinderTemplate import answerFinder
from answerFinderTemplate import checkQRcode
from answerFinderTemplate import sheetGenerator
from answerFinderTemplate import checkAnswerTest

# def generateTest():
#     questions_count = 30
#     student_id = 'a2CaDJim2E9JPyO'
#     questions_id = 'ahe27y32nc8238c'
#     lastname = "Sotvoldiyev"
#     firstname = "Axliyor"
#     info = "Fizika fanidan 3-oraliq nazorat ishi"
#     image = sheetGenerator(student_id, questions_id, questions_count, lastname, firstname, info)
#     cv2.imwrite('generated_template.png', image)
# generateTest()

dir = './test_template1/'
log = open(dir + 'log.txt', 'a')

def test(file):
    error, questions_count, student_id, questions_id, variant, answer, image = checkAnswerTest(dir + file)
    log.writelines(dir + file + '\n')
    if error:
        log.writelines('Image Error!\n')
        return False
    log.writelines('questions_count: ' + str(questions_count) + '\n')
    log.writelines('student_id: ' + student_id + '\n')
    log.writelines('questions_id: ' + questions_id + '\n')
    log.writelines('variant: ' + str(variant) + '\n')
    log.writelines('answer: ' + str(answer) + '\n')
    log.writelines(150*'-' + '\n')
    cv2.imwrite(dir + 'result_' + file, image)
    return True

test('image1.jpg')
test('image2.jpg')
test('image3.jpg')
test('image4.jpg')
test('image5.jpg')
test('image6.jpg')
test('image7.jpg')
test('image8.jpg')
test('image9.jpg')
log.close()