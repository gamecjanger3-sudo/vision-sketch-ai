import cv2
import mediapipe as mp
import numpy as np

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

print("Camera Opened:", cap.isOpened())

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

canvas = np.zeros((480, 640, 3), dtype=np.uint8)

prev_x, prev_y = 0, 0
draw_color = (255, 0, 0) # Blue

current_tool = "DRAW"

def fingers_up(handLms):
    tips = [8, 12, 16, 20]
    fingers = []

    for tip in tips:
        if handLms.landmark[tip].y < handLms.landmark[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers

print("Program started")
print("draw_color =", draw_color)

while True:
    success, img = cap.read()

    if not success or img is None:
        print("Camera not working")
        continue

    img = cv2.flip(img, 1)
    
    # Toolbar
    cv2.rectangle(img, (0, 0), (100, 50), (0, 0, 255), -1)
    cv2.rectangle(img, (100, 0), (200, 50), (0, 255, 0), -1)
    cv2.rectangle(img, (200, 0), (300, 50), (255, 0, 0), -1)
    cv2.rectangle(img, (300, 0), (450, 50), (50, 50, 50), -1)

    cv2.putText(img, "RED", (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7,
            (255,255,255), 2)

    cv2.putText(img, "GREEN", (110, 35),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7,
            (255,255,255), 2)

    cv2.putText(img, "BLUE", (220, 35),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7,
            (255,255,255), 2)
    
    cv2.putText(img, "ERASER", (310, 35),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7,
            (255,255,255), 2)

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

            fingers = fingers_up(handLms)

            
            
            h, w, _ = img.shape
            x = int(handLms.landmark[8].x * w)
            y = int(handLms.landmark[8].y * h)
            
            if prev_x == 0 and prev_y == 0:
                prev_x, prev_y = x, y

            # ✌ Selection Mode
            if fingers == [1, 1, 0, 0]:

                if y < 100:

                    if 0 < x < 100:
                        draw_color = (0, 0, 255)
                        current_tool = "DRAW"

                    elif 100 < x < 200:
                        draw_color = (0, 255, 0)
                        current_tool = "DRAW"

                    elif 200 < x < 300:
                        draw_color = (255, 0, 0)
                        current_tool = "DRAW"
                       

                    elif 300 < x < 450:
                        current_tool = "ERASER"

            # ☝ Draw Mode
            elif fingers == [1, 0, 0, 0]:

                if current_tool == "DRAW":
                    cv2.line(canvas,
                        (prev_x, prev_y),
                        (x, y),
                        draw_color,
                        8)

                elif current_tool == "ERASER":
                    cv2.circle(canvas,
                        (x, y),
                        30,
                        (0, 0, 0),
                        -1)
                prev_x, prev_y = x, y
            
    else:
        prev_x, prev_y = 0, 0

    img = cv2.add(img, canvas)
    
    cv2.circle(img, (600, 25), 20, draw_color, -1)
    cv2.putText(img,
            current_tool,
            (500, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255,255,255),
            2)
    cv2.imshow("AI Whiteboard", img)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

    elif key == ord('c'):
        canvas = np.zeros((480, 640, 3), dtype=np.uint8)
        prev_x, prev_y = 0, 0

    elif key == ord('r'):
        draw_color = (0, 0, 255)
        current_tool = "DRAW"
        print("Red")
        

    elif key == ord('g'):
        draw_color = (0, 255, 0)
        current_tool = "DRAW"
        print("Green")
        

    elif key == ord('b'):
        draw_color = (255, 0, 0)
        current_tool = "DRAW"
        print("Blue")
    elif key == ord('s'):
        cv2.imwrite("drawing.png", canvas)
        print("Drawing saved!")    
cap.release()
cv2.destroyAllWindows()