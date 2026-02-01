import os
import subprocess
import imageio_ffmpeg
from config import FRAMES_DIR, AUDIO_PATH

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


def extract_frames(video_path, fps=1):
    os.makedirs(FRAMES_DIR, exist_ok=True)

    for f in os.listdir(FRAMES_DIR):
        os.remove(os.path.join(FRAMES_DIR, f))

    cmd = [
        FFMPEG, "-y","-i", video_path,
        "-vf", f"fps={fps}",
        f"{FRAMES_DIR}/frame_%04d.jpg"
    ]

    subprocess.run(cmd, check=True)


def extract_audio(video_path):
    cmd = [
        FFMPEG, "-y","-i", video_path,
        "-ac", "1", "-ar", "16000",
        AUDIO_PATH
    ]

    subprocess.run(cmd, check=True)
