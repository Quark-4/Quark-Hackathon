import cv2
from deepface import DeepFace

camera = cv2.VideoCapture(0)

def detect_age():

    ret, frame = camera.read()

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

        if age < 18:
            person = "child"
        else:
            person = "adult"

        return {
            "status": "success",
            "age": age,
            "person": person,
            "confidence": result["face_confidence"]
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }