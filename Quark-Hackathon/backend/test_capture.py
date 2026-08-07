from screen_capture import capture_screen
from nsfw_detector import detect_nsfw

image = capture_screen()

print("Captured:", image)

result = detect_nsfw(image)

print("NSFW:", result)