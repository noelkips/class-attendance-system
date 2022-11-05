# import cv2
# import face_recognition

# img = cv2.imread("JOHN BETT.JPG")
# rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# img_encoding = face_recognition.face_encodings(rgb_img)[0]

# img1 = cv2.imread("WIFEY.JPG")
# rgb_img = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
# img_encoding1 = face_recognition.face_encodings(rgb_img)[0]

# result = face_recognition.compare_faces([img_encoding], img_encoding1)
# print("Result: ", result)


# cv2.imshow("Img", img)
# cv2.imshow("Img", img1)
# cv2.waitKey(0)