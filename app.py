import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="AiEdit Demo",
    page_icon="✨",
    layout="centered"
)

st.title("✨ AiEdit Image Editor (Demo Version)")
st.caption("Owner: Hamdan Studio")   # ✅ owner line
st.write("❌ No API • ❌ No Backend • ✅ Error-Free")

st.divider()

uploaded_file = st.file_uploader(
    "📤 Upload Image",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

st.divider()

prompt = st.text_input(
    "✍️ Enter prompt (demo only)",
    placeholder="make it anime, cinematic, HD..."
)

if st.button("✨ Generate AiEdit Image"):
    st.success("✅ Demo mode working")
    st.info("🔒 API disabled. This is UI demo only.")
