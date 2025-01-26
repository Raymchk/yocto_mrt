import cv2
import subprocess
import time

# Commande pour lancer libcamera-vid
libcamera_command = ["libcamera-vid", "-t", "0", "--inline", "--listen", "-o", "tcp://0.0.0.0:8554", "--width", "640", "--height", "480", "--framerate", "15"]

# Lancer libcamera-vid en arrière-plan
libcamera_process = subprocess.Popen(libcamera_command)
print("libcamera-vid lancé. Attente de 2 secondes pour l'initialisation...")
time.sleep(2)  # Attendre que le flux soit prêt


# Video stream IP address
stream_url = "tcp://192.168.1.78:8554"
cap = cv2.VideoCapture(stream_url)

# QR code detector
detector = cv2.QRCodeDetector()

while True:
    _, img = cap.read()
    if img is None:
        print("Failed to capture frame.")
        continue

    data, bbox, _ = detector.detectAndDecode(img)

    if bbox is not None and len(bbox) > 0:
        bbox = bbox.astype(int)  # Ensure bbox contains integer values
        for i in range(len(bbox[0])):
            pt1 = tuple(bbox[0][i])
            pt2 = tuple(bbox[0][(i + 1) % len(bbox[0])])
            cv2.line(img, pt1, pt2, color=(255, 0, 0), thickness=2)
        if data:
            cv2.putText(img, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 250, 120), 2)
            print("QR Code detected: ", data)

    cv2.imshow("QR Code Detector", img)
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
