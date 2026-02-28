import cv2
import pytesseract
from datetime import datetime
import csv
import os

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

registered_buses = [
    "TN45AB1234",
    "TN10CD5678",
    "TN22EF9999",
    "TN33GH0000",
    "TN55IJ1111",
    "TN66KL2222",
    "TN77MN3333"
]

last_detected = {}

file_name = "bus_entries.csv"

if not os.path.exists(file_name):
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Bus Number", "Date", "Time"])

cap = cv2.VideoCapture(0)

print("Camera Started... Press Q to Quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape

    x1 = int(w * 0.25)
    y1 = int(h * 0.4)
    x2 = int(w * 0.75)
    y2 = int(h * 0.6)

    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    roi = frame[y1:y2, x1:x2]

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    text = pytesseract.image_to_string(thresh, config=custom_config)

    clean_text = "".join(e for e in text if e.isalnum())

    cv2.putText(frame, f"Detected: {clean_text}", (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    if clean_text in registered_buses:

        current_time = datetime.now()

        if (clean_text not in last_detected or
            (current_time - last_detected[clean_text]).seconds > 10):

            date = current_time.strftime("%Y-%m-%d")
            time = current_time.strftime("%H:%M:%S")

            print(f"Bus {clean_text} Entered at {date} {time}")

            with open(file_name, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([clean_text, date, time])

            last_detected[clean_text] = current_time

        cv2.putText(frame,
                    f"ENTRY RECORDED: {clean_text}",
                    (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2)

    cv2.imshow("Bus Entry System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()