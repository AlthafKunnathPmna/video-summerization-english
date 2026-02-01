import streamlit as st
import tempfile
import os

from services.video_service import extract_frames, extract_audio
from services.audio_service import extract_important_audio
from services.vision_service import generate_captions
from services.ocr_service import extract_slide_logic
from services.llm_service import gemini_reason

st.set_page_config(page_title="Cross-Modal Video Notes AI")
st.title("🎓 Cross-Modal Video Notes Generator")

# ------------------ Upload ------------------
video = st.file_uploader(
    "Upload Lecture Video",
    type=["mp4", "mkv", "avi"]
)

# ------------------ Generate Button ------------------
generate = st.button("🚀 Generate Study Notes")

# ------------------ Run only on button press ------------------
if generate:

    if not video:
        st.warning("⚠️ Please upload a video first.")
        st.stop()

    audio_path = None

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(video.read())
        video_path = tmp.name

    try:
        with st.spinner("🎞 Processing video..."):
            extract_frames(video_path)
            audio_path = extract_audio(video_path)

        with st.spinner("🧠 Understanding audio..."):
            audio_text = extract_important_audio(audio_path)

        with st.spinner("👁 Understanding visuals..."):
            captions = generate_captions()
            visual_text = gemini_reason(
                "Summarize these visual descriptions:\n"
                + "\n".join(captions)
            )

        with st.spinner("📑 Reading slides..."):
            slide_text = extract_slide_logic()

        with st.spinner("🔗 Fusing modalities..."):
            fused = gemini_reason(f"""
AUDIO:
{audio_text}

VISUAL:
{visual_text}

SLIDES:
{slide_text}

Return structured study content.
""")

        with st.spinner("📝 Generating notes..."):
            notes = gemini_reason(f"""
Convert this into student notes.
Use headings, bullets, and key takeaways.

CONTENT:
{fused}
""")

        st.subheader("📘 Generated Study Notes")
        st.markdown(notes)

        st.download_button(
            "⬇️ Download Notes",
            notes,
            "video_notes.md",
            "text/markdown"
        )

    except Exception as e:
        st.error(str(e))

    finally:
        if os.path.exists(video_path):
            os.remove(video_path)
        if audio_path and os.path.exists(audio_path):
            os.remove(audio_path)
