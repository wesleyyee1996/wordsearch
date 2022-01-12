from imutils.object_detection import non_max_suppression
import numpy as np
import pytesseract
import argparse
import cv2
import time

img = cv2.imread('/home/pi/Downloads/test_word_hunt.jpg')
#img = cv2.imread('/home/pi/Downloads/Test_Word_Hunt_Small.png')

print(img.shape)
#img = img[500:1300, 1000:2000, :]
#img = img[120:300, 50:250, :]
edges = cv2.Canny(img, 100, 200)

#cv2.imshow("testcanny", edges)
#gray = cv2.cvtColor(edges, cv2.COLOR_BGR2GRAY)

thresh_inv = cv2.threshold(edges, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
#img = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)
blur = cv2.GaussianBlur(thresh_inv, (1,1), 0)

thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]

contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

mask = np.ones(img.shape[:2], dtype="uint8") * 255

cnt = 0
for c in contours:
    x, y, w, h = cv2.boundingRect(c)
    if w*h > 200 and w > 15 and h > 15:
        rect = cv2.rectangle(mask, (x-5, y-5), (x+w+5, y+h+5), (0, 0, 255), -1)
        #if cnt == 2:
        #    cv2.imshow('tst',img[x-5:x+w+5, y-5:y+h+5, :])
        #letter_img = img[x-w/2:x+w, y-h/2:y+h, :]
        #time.sleep(1)
        #print(pytesseract.image_to_string(rect, lang='eng', config='-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ --psm 11'))
    cnt += 1

res_final = cv2.bitwise_and(edges, edges, mask=cv2.bitwise_not(mask))

print(pytesseract.image_to_string(res_final, lang='eng', config='-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ --psm 11'))
#cv2.imshow('Result', img)
#cv2.imshow("boxes", mask)
cv2.imshow("output", res_final)
cv2.waitKey(0)

