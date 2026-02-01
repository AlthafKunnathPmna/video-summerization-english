import os
import easyocr
from config import FRAMES_DIR

reader = easyocr.Reader(['en'])


def extract_slide_logic(max_frames=5):
    points = []
    frames = sorted(os.listdir(FRAMES_DIR))[:max_frames]

    for frame in frames:
        results = reader.readtext(
            os.path.join(FRAMES_DIR, frame)
        )
        for _, text, conf in results:
            if conf > 0.6 and len(text) > 4:
                points.append(text)

    return " • ".join(dict.fromkeys(points))
