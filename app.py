import os
import base64
import requests
import streamlit as st
from PIL import Image
from io import BytesIO

# =========================
# AiEdit — Hamdan Studio
# =========================

st.set_page_config(page_title="AiEdit", page_icon="✨", layout="centered")

st.title("✨ AiEdit")
st.caption("AI photo editing web app built with Streamlit")

st.markdown(
    """
Upload **two photos**:
1) **Old photo (Child)**  
2) **Recent photo (Adult)**  

Then AiEdit will generate an image where **adult-you is holding child-you’s hand** naturally, with **soft background lighting** and a **smooth white background (#FFFFFF)**.
"""
)

# ---- Settings (placeholders for your "nano banana" model API)
# Option A: Put these in Streamlit Cloud Secrets or environment variables
# NANO_BANANA_API_URL = "https://your-api.com/generate"
# NANO_BANANA_API_KEY = "your_key_here"

NANO_BANANA_API_URL = os.getenv("NANO_BANANA_API_URL", "").strip()
NANO_BANANA_API_KEY = os.getenv("NANO_BANANA_API_KEY", "").strip()


def image_to_base64(img: Image.Image) -> str:
    """Convert PIL Image to base64 PNG string."""
    buf = BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")


def base64_to_image(b64: str) -> Image.Image:
    """Convert base64 string to PIL Image."""
    data = base64.b64decode(b64)
    return Image.open(BytesIO(data)).convert("RGB")


def build_prompt() -> str:
    # This is the main instruction prompt for your model
    return (
        "Create a realistic photo where the adult person from the recent photo is holding hands with "
        "the child from the old photo. Make it look natural, warm, and emotionally authentic. "
        "Match facial identity from each respective input. Ensure correct proportions (adult and child). "
        "Soft studio-like lighting, gentle shadows. Replace background with pure smooth white (#FFFFFF). "
        "No text, no watermark, no extra people. High detail, photorealistic."
    )


def call_nano_banana_api(child_img: Image.Image, adult_img: Image.Image) -> Image.Image:
    """
    Calls your 'nano banana' model API.
    You MUST provide:
      - NANO_BANANA_API_URL
      - NANO_BANANA_API_KEY (if needed)

    Expected API response format (example):
      { "image_base64": "<base64_png_or_jpg>" }

    If your API response differs, adjust parsing below.
    """
    if not NANO_BANANA_API_URL:
        raise RuntimeError(
            "API URL missing. Set NANO_BANANA_API_URL (env var / Streamlit secret) to your nano banana endpoint."
        )

    payload = {
        "prompt": build_prompt(),
        "child_image_base64": image_to_base64(child_img),
        "adult_image_base64": image_to_base64(adult_img),
        # optional knobs (if your backend supports)
        "background": "#FFFFFF",
        "soft_lighting": True,
    }

    headers = {"Content-Type": "application/json"}
    if NANO_BANANA_API_KEY:
        headers["Authorization"] = f"Bearer {NANO_BANANA_API_KEY}"

    resp = requests.post(NANO_BANANA_API_URL, json=payload, headers=headers, timeout=180)
    resp.raise_for_status()
    data = resp.json()

    # ---- adjust these keys based on your actual backend response
    img_b64 = data.get("image_base64") or data.get("output_base64") or data.get("result")
    if not img_b64:
        raise RuntimeError("API did not return image_base64. Check your backend response JSON keys.")

    return base64_to_image(img_b64)


# ---- Upload UI
col1, col2 = st.columns(2)

with col1:
    child_file = st.file_uploader("1) Upload old photo (Child)", type=["png", "jpg", "jpeg"])

with col2:
    adult_file = st.file_uploader("2) Upload recent photo (Adult)", type=["png", "jpg", "jpeg"])

child_img = None
adult_img = None

if child_file:
    child_img = Image.open(child_file).convert("RGB")
    st.image(child_img, caption="Child photo preview", use_container_width=True)

if adult_file:
    adult_img = Image.open(adult_file).convert("RGB")
    st.image(adult_img, caption="Adult photo preview", use_container_width=True)

st.divider()

generate = st.button("✨ Generate AiEdit Image", use_container_width=True)

if generate:
    if not child_img or not adult_img:
        st.error("Please upload BOTH photos (Child + Adult) first.")
    else:
        with st.spinner("Generating... (model is working)"):
            try:
                out_img = call_nano_banana_api(child_img, adult_img)
                st.success("Done ✅")
                st.image(out_img, caption="AiEdit Output", use_container_width=True)

                # Download
                buf = BytesIO()
                out_img.save(buf, format="PNG")
                st.download_button(
                    "⬇️ Download PNG",
                    data=buf.getvalue(),
                    file_name="aiedit_output.png",
                    mime="image/png",
                    use_container_width=True,
                )

            except requests.HTTPError as e:
                st.error("API error. Please check your API URL/Key and backend logs.")
                st.exception(e)
            except Exception as e:
                st.error("Something went wrong.")
                st.exception(e)

st.divider()
st.caption("Owner: Hamdan Studio")
