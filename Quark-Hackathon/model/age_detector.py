import cv2
from deepface import DeepFace

camera = cv2.VideoCapture(0)

while True:

    ret, frame = camera.read()

    if not ret:
        break

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
            status = "Child"
            color = (0,0,255)
        else:
            status = "Adult"
            color = (0,255,0)

        x = result["region"]["x"]
        y = result["region"]["y"]
        w = result["region"]["w"]
        h = result["region"]["h"]

        cv2.rectangle(frame,(x,y),(x+w,y+h),color,2)

        cv2.putText(
            frame,
            f"{status} ({age})",
            (x,y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )

    except Exception as e:
        print(e)

    cv2.imshow("AI Guardian", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()