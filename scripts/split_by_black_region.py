import cv2
import os
import json

train_number = "12309"

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.dirname(BASE_PATH)
video_path = os.path.join(ROOT_PATH, "Raw_video", "input_video.mp4")
output_base = os.path.join(ROOT_PATH, "processed_video", f"{train_number}")
rect_file = os.path.join(BASE_PATH, "rect.json")  # rectangle instead of dots

os.makedirs(output_base, exist_ok=True)

# Load rectangle region (x1, y1, x2, y2)
with open(rect_file, "r") as f:
    rect = json.load(f)  # e.g. [100, 200, 200, 300]

cap = cv2.VideoCapture(video_path)
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*"mp4v")

def is_black(frame, rect, threshold=50):
    """Check if rectangular region is dark enough."""
    x1, y1, x2, y2 = rect
    roi = frame[y1:y2, x1:x2]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    avg_brightness = gray.mean()
    return avg_brightness < threshold

coach_id = 1
out = None
in_gap = True
frame_count = 0
screenshot1_saved = False
folder = None

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame_count += 1

    if is_black(frame, rect):  # GAP detected
        if not in_gap and out is not None:
            out.release()
            print(f"✅ Saved Coach {coach_id}")

            # ---- Extract middle screenshot ----
            coach_video = os.path.join(folder, f"{train_number}_{coach_id}.mp4")
            cap_coach = cv2.VideoCapture(coach_video)
            total_frames = int(cap_coach.get(cv2.CAP_PROP_FRAME_COUNT))
            middle_frame = total_frames // 2

            cap_coach.set(cv2.CAP_PROP_POS_FRAMES, middle_frame)
            ret2, mid_frame = cap_coach.read()
            if ret2:
                screenshot_path = os.path.join(folder, f"{train_number}_{coach_id}_2.jpg")
                cv2.imwrite(screenshot_path, mid_frame)
                print(f"📸 Screenshot 2 saved (mid): {screenshot_path}")

            cap_coach.release()
            # -----------------------------------

            coach_id += 1
            out = None
        in_gap = True
        screenshot1_saved = False
    else:  # inside a coach
        if in_gap or out is None:  # new coach starts
            folder = os.path.join(output_base, f"{train_number}_{coach_id}")
            os.makedirs(folder, exist_ok=True)
            filename = os.path.join(folder, f"{train_number}_{coach_id}.mp4")
            out = cv2.VideoWriter(filename, fourcc, fps, (width, height))
            in_gap = False
            screenshot1_saved = False

        if out is not None:
            out.write(frame)

            # First screenshot (front of coach)
            if not screenshot1_saved:
                screenshot_path = os.path.join(folder, f"{train_number}_{coach_id}_1.jpg")
                cv2.imwrite(screenshot_path, frame)
                print(f"📸 Screenshot 1 saved (front): {screenshot_path}")
                screenshot1_saved = True

cap.release()
if out is not None:
    out.release()

print(f" Splitting finished. Total coaches: {coach_id}")
