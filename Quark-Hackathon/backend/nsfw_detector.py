from nudenet import NudeDetector

# Load the model once
detector = NudeDetector()

def detect_nsfw(image_path):
    try:
        results = detector.detect(image_path)

        print("Detection Results:", results)

        # If any explicit class is detected with decent confidence
        for item in results:
            print(item)

            if item["score"] > 0.2:
             return True

        return False

    except Exception as e:
        print("NSFW Detection Error:", e)
        return False