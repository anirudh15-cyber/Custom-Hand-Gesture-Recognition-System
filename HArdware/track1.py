import cv2
import time
import HModule as htm
import pyfirmata

pins = [7, 8, 9, 10]           # relay connected to pins of Arduino
pin_i = 0
port = 'COM4'                 
board = pyfirmata.Arduino(port)

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

pTime = 0

detector = htm.handDetector(detectionCon=0.75)

tipIds = [4, 8, 12, 16, 20]

finger_states = {
    0: {'text': '0', 'label': 'LOW', 'pin': 0},
    1: {'text': '1', 'label': 'HI-1', 'pin': 1},
    2: {'text': '2', 'label': 'HI-2', 'pin': 2},
    3: {'text': '3', 'label': 'HI-3', 'pin': 3},
}

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        fingers = []

        # Thumb
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 Fingers
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        finger_state = fingers.count(1)
        print(finger_state)
        if finger_state == 0 :
            cv2.rectangle(img, (20, 225), (170, 460), (255, 0, 0), cv2.FILLED)
            cv2.putText(img, "0", (45, 375), cv2.FONT_HERSHEY_PLAIN,
                    10, (0, 255, 255), 25)
            cv2.putText(img, "LOW", (52, 425), cv2.FONT_HERSHEY_PLAIN,
                    3, (0, 255, 255), 3)
            board.digital[pins[pin_i]].write(finger_state)
        elif finger_state in finger_states:
            state = finger_states[finger_state]
            cv2.rectangle(img, (20, 225), (170, 460), (255, 0, 0), cv2.FILLED)
            cv2.putText(img, state['text'], (45, 375), cv2.FONT_HERSHEY_PLAIN, 10, (0, 255, 255), 25)
            cv2.putText(img, state['label'], (47, 425), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 255), 3)
            pin_i = state['pin']
            board.digital[pins[pin_i]].write(1)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()
