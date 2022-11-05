from turtle import right
import cv2
import face_recognition

from simple_facerec import SimpleFacerec

sfr = SimpleFacerec()
sfr.load_encoding_images("images/")

cap = cv2.VideoCapture(0)


while True:
    ret, frame = cap.read()
    
    face_locations, face_names = sfr.detect_known_faces(frame)
    
    for face_loc, name in zip(face_locations, face_names):
        y1, x2, y2, x1 = (face_loc)

        cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)

        cv2.rectangle(frame, (x1, y1), (x2,y2), (0, 0, 200), 4)
        print(name)
        # if matches == True:
        #     print('cool')

        # else:
        #     print('no')
    
    cv2.imshow("Frame", frame)

    Key = cv2.waitKey(1)
    if Key == 27:
        break

cap.release()
cv2.destroyAllWindows()