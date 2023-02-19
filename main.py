from answerFinderLib import answerFinder
paths = [
    ["template/test1.jpg", 90],
    ["template/test2.jpg", 90],
    ["template/test3.jpg", 90]
]

for x in paths:    
    variant, answer, error = answerFinder(x[0], x[1])
    print('Variant:', variant)
    print('Error:', error)
    if not error:
        print('Answer:',answer)
