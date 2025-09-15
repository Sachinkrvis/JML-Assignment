import cv2
import json
import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.dirname(BASE_PATH)


video_path = os.path.join(ROOT_PATH, "Raw_video", "input_video.mp4")
output_file = os.path.join(BASE_PATH, "rect.json")


# Open video and grab first frame
cap = cv2.VideoCapture(video_path)
ret, frame = cap.read()
cap.release()

if not ret:
    print("❌ Could not read video")
    exit()

rect = []  # will hold [x1, y1, x2, y2]
drawing = False
x1, y1 = -1, -1

def mouse_callback(event, x, y, flags, param):
    global x1, y1, rect, drawing, frame, clone

    if event == cv2.EVENT_LBUTTONDOWN:
        # First click: start point
        drawing = True
        x1, y1 = x, y

    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        # Draw rectangle dynamically
        temp = clone.copy()
        cv2.rectangle(temp, (x1, y1), (x, y), (0, 0, 255), 2)
        cv2.imshow("Select Black Region", temp)

    elif event == cv2.EVENT_LBUTTONUP:
        # Second click: end point
        drawing = False
        rect = [x1, y1, x, y]
        cv2.rectangle(frame, (x1, y1), (x, y), (0, 0, 255), 2)
        cv2.imshow("Select Black Region", frame)

clone = frame.copy()
cv2.namedWindow("Select Black Region", cv2.WINDOW_NORMAL)
cv2.imshow("Select Black Region", frame)
cv2.setMouseCallback("Select Black Region", mouse_callback)

print("👉 Drag with left mouse button to select rectangle. Press 'q' when done.")

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cv2.destroyAllWindows()

if rect:
    # Normalize coordinates (make sure x1<x2, y1<y2)
    x1, y1, x2, y2 = rect
    rect = [min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)]

    with open(output_file, "w") as f:
        json.dump(rect, f)

    print(f"✅ Saved rectangle {rect} to {output_file}")
else:
    print("⚠️ No rectangle selected")
