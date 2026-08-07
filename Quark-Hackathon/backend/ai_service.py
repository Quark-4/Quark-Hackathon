import cv2
import time
from deepface import DeepFace
from screen_capture import capture_screen
from nsfw_detector import detect_nsfw


def detect_age():

    camera = cv2.VideoCapture(0)

    ret, frame = camera.read()

    camera.release()

    if not ret:
        return {
            "status": "error",
            "message": "Camera not available"
        }

    try:
        result = DeepFace.analyze(
            img_path=frame,
            actions=["age"],
            detector_backend="opencv",
            enforce_detection=False,
            silent=True
        )

        if isinstance(result, list):
            result = result[0]

        age = int(result["age"])

        # Determine person type
        if age < 18:
            person = "child"
        else:
            person = "child"

        # Capture the current screen
        # Wait for page/video rendering
        time.sleep(3)

        image = capture_screen()

        # Detect explicit content
        nsfw = detect_nsfw(image)

        return {
            "status": "success",
            "age": age,
            "person": person,
            "nsfw": nsfw,
            "confidence": result.get("face_confidence", 0)
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }