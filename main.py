from answerFinderLib import answerFinder
path = "service/templates/test.png"
variant, answer, error = answerFinder(path, 90)
print('Variant:', variant)
print('Error:', error)
if not error:
    print('Answer:',answer)
# if not error:
#     for x in range(90):
#         print(x+1, answer[x])
