from pynput import mouse
import mss
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import re
import pytesseract
import cv2
import numpy as np

def get_bounds(clicks=2):
    counter = 0
    bounds = []
    # print("BOUND 1")

    def on_click(x, y, button, pressed):
        nonlocal counter
        
        if pressed:
            counter += 1
            bounds.append((x, y))
            
            # if counter == 1:
            #     print("BOUND 2")
            if counter == clicks:
                return False

    with mouse.Listener(on_click=on_click) as listener:
        listener.join()
    return bounds

def capture_region(bounds):
    x1 = bounds[0][0]
    y1 = bounds[0][1]
    x2 = bounds[1][0]
    y2 = bounds[1][1]

    if (x1 > x2):
        x1, x2 = x2, x1
    if (y1 > y2):
        y1, y2 = y2, y1

    region = {
        "top": y1,
        "left": x1,
        "width": x2 - x1,
        "height": y2 - y1
    }

    mss_img = mss.mss().grab(region)
    return Image.frombytes("RGB", mss_img.size, mss_img.rgb)

def preprocess_image(img):
    # Convert PIL Image to OpenCV format (numpy array)
    img_cv = np.array(img)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img_cv, cv2.COLOR_RGB2GRAY)
    
    # Apply thresholding
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    
    # Remove noise using GaussianBlur
    blurred = cv2.GaussianBlur(thresh, (5, 5), 0)
    
    # Convert back to PIL Image
    return Image.fromarray(blurred)

def extract_text_from_image(img):
    try:
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(img, config=custom_config, lang='eng')
        return text
    except Exception as e:
        return f"An error occurred: {e}"

def format(text):
    # remove special characters, remove (*)
    text = re.sub(r"5\]", "\n", text)
    text = re.sub(r"[^\w\s+:)(-+]", "\n", text)
    text = re.sub(r"\([^)]*\)", "", text)

    # normalize whitespace, preserving newlines remove blank lines
    lines = text.splitlines()
    cleaned_lines = [re.sub(r"\s+", " ", line) for line in lines]
    cleaned_lines = [line.strip() for line in lines if line]
    text = '\n'.join(cleaned_lines)

    return text

print("Click")
bounds = get_bounds()
print("Processing...")

screenshot = capture_region(bounds)
# screenshot.save("img.png")

img = preprocess_image(screenshot)

text = extract_text_from_image(img)
text = format(text)

print(text)