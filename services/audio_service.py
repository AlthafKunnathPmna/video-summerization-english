import whisper
import re
from config import AUDIO_PATH

model = whisper.load_model("base")


def clean_text(text):
    fillers = ["uh", "um", "you know", "okay", "so"]
    for f in fillers:
        text = text.replace(f, "")
    return re.sub(r"\s+", " ", text).strip()


def extract_important_audio():
    result = model.transcribe(AUDIO_PATH)
    important = []

    for seg in result["segments"]:
        if len(seg["text"]) > 30:
            important.append(clean_text(seg["text"]))

    return " ".join(important)
