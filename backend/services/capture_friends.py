from pynput import mouse
import mss
from PIL import Image
import pytesseract as tess

def record():
    bounds = get_bounds()
    print("Processing...")

    for i in range(5000):
        img = capture_region(bounds)
        img.save('img.png')
        with open('img.txt', 'a') as file:
            file.write(tess.image_to_string('img.png'))

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
    return Image.frombytes('RGB', mss_img.size, mss_img.rgb)

def print_originals():
    lines = {}
    with open('img.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if line not in lines:
                lines[line] = 0
            lines[line] += 1
    
    for line, count in lines.items():
        print(f"{count}:::{line}")

print_originals()