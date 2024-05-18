import cv2


def run():
    cap = cv2.VideoCapture("tcp://192.168.152.202:8888/")

    if not cap.isOpened():
        print("Error: Unable to open video stream")
        exit()

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Unable to read frame from video stream")
            break

        cv2.imshow("Video Stream", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
