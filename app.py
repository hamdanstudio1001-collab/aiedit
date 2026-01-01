import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="AiEdit Age Transformation (Demo)",
    page_icon="✨",
    layout="centered"
)

st.title("✨ AiEdit Age Transformation (Demo)")
st.caption("Owner: Hamdan Studio")
st.write("❌ No API • ❌ No Backend • ✅ Error-Free")

st.divider()

st.subheader("👶 Upload Childhood Photo")
child_img = st.file_uploader(
    "Bachpan ki photo upload karo",
    type=["png", "jpg", "jpeg"],
    key="child"
)

st.subheader("🧑 Upload Adult Photo")
adult_img = st.file_uploader(
    "Jawani ki photo upload karo",
    type=["png", "jpg", "jpeg"],
    key="adult"
)

if child_img and adult_img:
    col1, col2 = st.columns(2)

    with col1:
        st.image(
            Image.open(child_img),
            caption="👶 Childhood",
            use_column_width=True
        )

    with col2:
        st.image(
            Image.open(adult_img),
            caption="🧑 Adult",
            use_column_width=True
        )

    st.success("✅ Both images uploaded successfully")

st.divider()

if st.button("✨ Generate Age Transformation"):
    st.warning("⚠️ Demo mode")
    st.info("Real AI transformation API baad me connect hogi")
    st.success("UI ready for Bachpan ➜ Jawani feature 🚀")
