import cv2

for index in [0, 1]:
    print(f"\nTesting camera {index}")

    cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)

    print("Opened:", cap.isOpened())

    ret, frame = cap.read()

    print("Read frame:", ret)

    cap.release()