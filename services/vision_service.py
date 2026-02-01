import os
import torch
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from config import FRAMES_DIR

device = "cuda" if torch.cuda.is_available() else "cpu"

processor = BlipProcessor.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)
model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
).to(device)
model.eval()


def generate_captions(max_frames=6):
    captions = []
    frames = sorted(os.listdir(FRAMES_DIR))[:max_frames]

    for frame in frames:
        image = Image.open(
            os.path.join(FRAMES_DIR, frame)
        ).convert("RGB")

        inputs = processor(image, return_tensors="pt").to(device)

        with torch.no_grad():
            output = model.generate(**inputs, max_length=30)

        captions.append(
            processor.decode(output[0], skip_special_tokens=True)
        )

    return captions
