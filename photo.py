import cv2
import numpy as np
import time

# Load Haar cascades for liveliness
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade  = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Open webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Failed to open webcam")
    exit()

height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
center_x, center_y = width // 2, height // 2
radius = min(center_x, center_y) - 50  # circular area

# Countdown 3…2…1
for i in range(3, 0, -1):
    ret, frame = cap.read()
    if not ret:
        continue
    
    # Circular mask
    mask = np.zeros_like(frame, dtype=np.uint8)
    cv2.circle(mask, (center_x, center_y), radius, (1,1,1), -1)
    circular_frame = frame * mask + 255 * (1 - mask)

    # Draw "+" at center
    cv2.drawMarker(circular_frame, (center_x, center_y), color=(0,0,255), 
                   markerType=cv2.MARKER_CROSS, markerSize=20, thickness=2)

    # Show countdown number
    cv2.putText(circular_frame, str(i), (center_x-25, center_y-100), 
                cv2.FONT_HERSHEY_SIMPLEX, 3, (0,0,255), 5, cv2.LINE_AA)

    cv2.imshow("Align Yourself", circular_frame)
    cv2.waitKey(1000)  # wait 1 second per count

# Capture photo after countdown
ret, frame = cap.read()
cap.release()
if not ret:
    print("Failed to capture frame")
    cv2.destroyAllWindows()
    exit()

# Circular mask for final photo (without "+")
mask = np.zeros_like(frame, dtype=np.uint8)
cv2.circle(mask, (center_x, center_y), radius, (1,1,1), -1)
user_photo = frame * mask + 255 * (1 - mask)

# Save photo
photo_filename = "user.png"
cv2.imwrite(photo_filename, user_photo)
print(f"Photo saved as {photo_filename}")

# Show final photo for 5 seconds
cv2.imshow("Captured Photo", user_photo)
cv2.waitKey(5000)
cv2.destroyAllWindows()

# ---------------- Liveliness Detection with Circle Check -----------------
gray = cv2.cvtColor(user_photo, cv2.COLOR_BGR2GRAY)
gray = cv2.equalizeHist(gray)
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

if len(faces) == 0:
    print("No face detected ❌ - FAKE")
else:
    liveliness_detected = False
    outside_circle = False

    for (x, y, w, h) in faces:
        # Check if face is fully inside the circular area
        face_corners = [(x, y), (x+w, y+h)]
        for (fx, fy) in face_corners:
            if (fx - center_x)**2 + (fy - center_y)**2 > radius**2:
                outside_circle = True
                break
        if outside_circle:
            break

        # Check eyes for liveliness
        face_roi = gray[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(face_roi)
        if len(eyes) >= 1:
            liveliness_detected = True

    if outside_circle:
        print("User outside circular area ❌ - FAKE")
    elif liveliness_detected:
        print("User is LIVE ✅")
    else:
        print("User is FAKE ❌")
