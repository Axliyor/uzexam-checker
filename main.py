from answerFinderLib import answerFinder
# path = "template/template1Test.png"
path = "template/7.jpg"
variant, answer, error = answerFinder(path, 90)
print('Variant:', variant)
print('Error:', error)
# if not error:
#     print('Answer:',answer)
if not error:
    for x in range(90):
        print(x+1, answer[x])
