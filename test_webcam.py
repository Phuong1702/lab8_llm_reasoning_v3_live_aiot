import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Không mở được webcam. Thử đổi camera index 0 thành 1.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Không đọc được frame từ webcam.")
        break

    cv2.imshow("Lab 8 Webcam Test - Press Q to quit", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()