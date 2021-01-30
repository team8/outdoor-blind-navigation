import cv2
import imutils

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

person = cv2.imread("person.jpg")
annotated_person = person.copy()
(rects, weights) = hog.detectMultiScale(person, winStride=(4, 4), padding=(8, 8), scale=1.05)

for (x, y, w, h) in rects:
    cv2.rectangle(annotated_person, (x, y), (x + w, y + h), (0, 0, 255), 2)

cv2.imshow("person", annotated_person)
cv2.waitKey(10000)

