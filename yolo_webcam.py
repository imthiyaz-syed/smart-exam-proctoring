import time
from collections import deque

import cv2
import tkinter as tk
from tkinter import messagebox
from ultralytics import YOLO

# ==================== SHARED STATE (for app.py) ====================
MAX_WARNINGS = 3

proctoring_state = {
    "active": False,
    "cheating_flag": False,
    "multiple_faces": False,
    "no_face": False,
    "looking_away": False,
    "looking_side": False,
    "looking_down": False,
    "status": "Idle",
    "face_count": 0,
    "detected_objects": [],
    "head_orientation": "N/A",
    "eyes_visible": False,
    "alert_shown": False,
    "warnings": 0,
    "phone_detections": 0,
    "violations_count": 0,
    "exam_terminated": False,
    "termination_reason": "",
    "last_violation": "",
}
# ===================================================================


model_path = "yolov8_saved_model.pt"
model = YOLO(model_path)
model.conf = 0.5
model.iou = 0.5


face_count_history = deque(maxlen=30)
cheating_alert_shown = False
multiple_faces_alert_shown = False


def show_alert(message, title="Alert"):
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    messagebox.showwarning(title, message)
    root.destroy()


def reset_proctoring_state():
    global cheating_alert_shown, multiple_faces_alert_shown

    cheating_alert_shown = False
    multiple_faces_alert_shown = False
    face_count_history.clear()

    proctoring_state["active"] = True
    proctoring_state["cheating_flag"] = False
    proctoring_state["multiple_faces"] = False
    proctoring_state["no_face"] = False
    proctoring_state["looking_away"] = False
    proctoring_state["looking_side"] = False
    proctoring_state["looking_down"] = False
    proctoring_state["status"] = "Running"
    proctoring_state["face_count"] = 0
    proctoring_state["detected_objects"] = []
    proctoring_state["head_orientation"] = "Straight"
    proctoring_state["eyes_visible"] = False
    proctoring_state["alert_shown"] = False
    proctoring_state["warnings"] = 0
    proctoring_state["phone_detections"] = 0
    proctoring_state["violations_count"] = 0
    proctoring_state["exam_terminated"] = False
    proctoring_state["termination_reason"] = ""
    proctoring_state["last_violation"] = ""


def register_violation(reason, terminate=False):
    proctoring_state["last_violation"] = reason
    proctoring_state["violations_count"] += 1
    proctoring_state["status"] = reason

    if reason == "Cell Phone":
        proctoring_state["phone_detections"] += 1

    if terminate:
        proctoring_state["warnings"] = MAX_WARNINGS
        proctoring_state["exam_terminated"] = True
        proctoring_state["termination_reason"] = reason
        proctoring_state["active"] = False
        return

    proctoring_state["warnings"] = min(MAX_WARNINGS, proctoring_state["warnings"] + 1)
    if proctoring_state["warnings"] >= MAX_WARNINGS:
        proctoring_state["exam_terminated"] = True
        proctoring_state["termination_reason"] = reason
        proctoring_state["active"] = False


def live_webcam_detection():
    global cheating_alert_shown, multiple_faces_alert_shown

    reset_proctoring_state()

    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cam.set(cv2.CAP_PROP_FPS, 30)
    cam.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    head_orientation = "Straight"
    detected_objects = set()
    cheating_flag = False
    multiple_faces_detected = False
    phone_detected_count = 0
    face_count = 0
    no_face_count = 0
    looking_away_count = 0
    side_look_streak = 0
    down_look_streak = 0

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    eye_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_eye.xml"
    )

    print("YOLO Proctoring Started - Press 'q' to exit")

    while cam.isOpened():
        if proctoring_state.get("exam_terminated"):
            break

        ret, frame = cam.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = model.predict(rgb_frame, stream=True, verbose=False)

        current_frame_objects = set()
        current_face_count = 0
        phone_detected = False

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces_haar = face_cascade.detectMultiScale(gray, 1.1, 4)
        haar_face_count = len(faces_haar)
        frame_height, frame_width = frame.shape[:2]
        primary_face = max(faces_haar, key=lambda face: face[2] * face[3]) if haar_face_count else None
        proctoring_state["eyes_visible"] = False

        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                object_name = model.names[class_id]
                current_frame_objects.add(object_name)

                if class_id == 0:
                    current_face_count += 1
                    detected_objects.add("person")
                    color = (0, 255, 0)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(
                        frame,
                        f"Person {confidence:.2f}",
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        color,
                        2,
                    )

                elif class_id == 67:
                    phone_detected = True
                    detected_objects.add("cell phone")
                    color = (0, 0, 255)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)
                    cv2.putText(
                        frame,
                        f"CELL PHONE {confidence:.2f}",
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        color,
                        2,
                    )
                    cv2.putText(
                        frame,
                        "CHEATING DETECTED",
                        (50, 100),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        3,
                    )

                elif class_id == 63:
                    detected_objects.add("laptop")
                    color = (0, 165, 255)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(
                        frame,
                        f"Laptop {confidence:.2f}",
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        color,
                        2,
                    )

                elif class_id == 73:
                    detected_objects.add("book")
                    color = (255, 0, 255)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(
                        frame,
                        f"Book {confidence:.2f}",
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        color,
                        2,
                    )

                else:
                    detected_objects.add(object_name)
                    color = (128, 128, 128)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 1)
                    cv2.putText(
                        frame,
                        f"{object_name} {confidence:.2f}",
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.4,
                        color,
                        1,
                    )

        for (x, y, w, h) in faces_haar:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 1)

        if primary_face is not None:
            x, y, w, h = primary_face
            face_center_x = x + (w // 2)
            face_center_y = y + (h // 2)
            frame_center_x = frame_width // 2
            side_threshold = max(30, int(frame_width * 0.10))
            down_threshold = int(frame_height * 0.56)

            face_roi = gray[max(y, 0):max(y + h, 0), max(x, 0):max(x + w, 0)]
            eyes_visible = False

            if face_roi.size > 0:
                eyes = eye_cascade.detectMultiScale(face_roi, 1.1, 4)
                eyes_visible = len(eyes) > 0
                proctoring_state["eyes_visible"] = eyes_visible

                for (ex, ey, ew, eh) in eyes[:2]:
                    cv2.rectangle(
                        frame,
                        (x + ex, y + ey),
                        (x + ex + ew, y + ey + eh),
                        (255, 255, 0),
                        1,
                    )

            if face_center_y > down_threshold or (not eyes_visible and face_center_y > int(frame_height * 0.50)):
                head_orientation = "Looking Down"
                down_look_streak += 1
                side_look_streak = max(0, side_look_streak - 1)
                looking_away_count += 1
            elif face_center_x < frame_center_x - side_threshold:
                head_orientation = "Looking Left"
                side_look_streak += 1
                down_look_streak = max(0, down_look_streak - 1)
                looking_away_count += 1
            elif face_center_x > frame_center_x + side_threshold:
                head_orientation = "Looking Right"
                side_look_streak += 1
                down_look_streak = max(0, down_look_streak - 1)
                looking_away_count += 1
            else:
                head_orientation = "Straight"
                side_look_streak = max(0, side_look_streak - 2)
                down_look_streak = max(0, down_look_streak - 2)
                looking_away_count = max(0, looking_away_count - 2)

            cv2.putText(
                frame,
                f"Head: {head_orientation}",
                (x, max(25, y - 12)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 0),
                2,
            )
            cv2.putText(
                frame,
                f"Eyes: {'Visible' if proctoring_state['eyes_visible'] else 'Not Clear'}",
                (x, min(frame_height - 10, y + h + 18)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                (255, 255, 0),
                1,
            )

        face_count = max(current_face_count, haar_face_count)
        face_count_history.append(face_count)

        proctoring_state["face_count"] = face_count
        proctoring_state["detected_objects"] = list(current_frame_objects)
        proctoring_state["head_orientation"] = head_orientation

        avg_face_count = sum(face_count_history) / len(face_count_history) if face_count_history else 0
        if avg_face_count > 1.5:
            multiple_faces_detected = True
            proctoring_state["multiple_faces"] = True
            cv2.putText(
                frame,
                "MULTIPLE FACES DETECTED",
                (50, 140),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2,
            )
            if not multiple_faces_alert_shown:
                show_alert(
                    "Multiple faces detected.\n\nOnly one person should be visible during the exam.",
                    "Warning",
                )
                multiple_faces_alert_shown = True
                register_violation("Multiple Faces")
        else:
            proctoring_state["multiple_faces"] = False

        if face_count == 0:
            no_face_count += 1
            proctoring_state["no_face"] = True
            cv2.putText(
                frame,
                "NO FACE DETECTED",
                (50, 180),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 165, 255),
                2,
            )
            if no_face_count == 30:
                register_violation("No Face")
        else:
            no_face_count = max(0, no_face_count - 1)
            proctoring_state["no_face"] = False

        if phone_detected:
            phone_detected_count += 1
            if phone_detected_count >= 3:
                cheating_flag = True
                proctoring_state["cheating_flag"] = True
                register_violation("Cell Phone", terminate=True)
                if not cheating_alert_shown and not proctoring_state["alert_shown"]:
                    show_alert(
                        "Cell phone detected.\n\nCheating attempt recorded.\nExam will be terminated.",
                        "Cheating Detected",
                    )
                    cheating_alert_shown = True
                    proctoring_state["alert_shown"] = True
                break
        else:
            phone_detected_count = max(0, phone_detected_count - 1)

        if looking_away_count > 15:
            proctoring_state["looking_away"] = True
            proctoring_state["looking_side"] = side_look_streak >= 12
            proctoring_state["looking_down"] = down_look_streak >= 10
            cv2.putText(
                frame,
                "LOOKING AWAY FREQUENTLY",
                (50, 220),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 165, 0),
                2,
            )
            if side_look_streak >= 12 and not proctoring_state["exam_terminated"]:
                register_violation("Looking Side", terminate=True)
                if not proctoring_state["alert_shown"]:
                    show_alert(
                        "Repeated side looking detected.\n\nExam will be terminated.",
                        "Security Alert",
                    )
                    proctoring_state["alert_shown"] = True
                break
            if down_look_streak >= 10 and not proctoring_state["exam_terminated"]:
                register_violation("Looking Down", terminate=True)
                if not proctoring_state["alert_shown"]:
                    show_alert(
                        "Repeated downward looking detected.\n\nExam will be terminated.",
                        "Security Alert",
                    )
                    proctoring_state["alert_shown"] = True
                break
            if looking_away_count == 16:
                register_violation("Looking Away")
        else:
            proctoring_state["looking_away"] = False
            proctoring_state["looking_side"] = False
            proctoring_state["looking_down"] = False

        cv2.putText(
            frame,
            f"Faces: {face_count}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
        )
        cv2.putText(
            frame,
            f"Warnings: {proctoring_state['warnings']}/{MAX_WARNINGS}",
            (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 255),
            2,
        )
        cv2.putText(
            frame,
            f"Side/Down: {side_look_streak}/{down_look_streak}",
            (10, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 255),
            1,
        )
        cv2.putText(
            frame,
            f"Objects: {', '.join(sorted(current_frame_objects))}",
            (10, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (200, 200, 200),
            1,
        )
        cv2.putText(
            frame,
            "Press 'q' to quit",
            (10, frame.shape[0] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1,
        )

        cv2.imshow("YOLO Proctoring", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    cam.release()
    cv2.destroyAllWindows()

    if proctoring_state["exam_terminated"]:
        status = proctoring_state["termination_reason"] or "Terminated"
    elif cheating_flag:
        status = "Cell Phone"
    elif multiple_faces_detected:
        status = "Multiple Faces"
    elif no_face_count > 30:
        status = "No Face"
    elif looking_away_count > 20:
        status = "Looking Away"
    else:
        status = "Completed"

    proctoring_state["active"] = False
    proctoring_state["status"] = status
    proctoring_state["cheating_flag"] = cheating_flag
    proctoring_state["face_count"] = face_count

    return head_orientation, list(detected_objects), cheating_flag, status, face_count


if __name__ == "__main__":
    head, objects, cheating, status, face_count = live_webcam_detection()
    print(f"Head Orientation: {head}")
    print(f"Detected Objects: {objects}")
    print(f"Cheating Detected: {cheating}")
    print(f"Status: {status}")
    print(f"Face Count: {face_count}")
    print("Proctoring session ended.")
