scores = open("test.txt","r")
test = scores.readline()
scores.close()
test= test.split(" ")
test[1] = test[1].strip()

print test[1]

