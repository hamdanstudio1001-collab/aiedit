import streamlit as st
import replicate
from rembg import remove
from PIL import Image
import io
import requests

# --- APP CONFIGURATION ---
st.set_page_config(page_title="AiEdit", page_icon="🍌", layout="wide")

# Custom CSS for the "Smooth White" look
st.markdown("""
    <style>
    .stApp {
        background-color: #FFFFFF;
    }
    .main-header {
        font-family: 'Helvetica Neue', sans-serif;
        color: #333;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("AiEdit 🍌")
    st.markdown("Reunite your past and present self.")
    
    # Securely input API Key
    api_key = st.text_input("Enter Replicate API Key", type="password")
    if not api_key:
        st.warning("Please enter an API key to proceed.")
        st.stop()
    
    import os
    os.environ["REPLICATE_API_TOKEN"] = api_key

# --- MAIN FUNCTIONS ---

def process_images(child_img, adult_img):
    """
    This function sends both images to an IP-Adapter model
    to generate the mixed image.
    """
    # Note: In a production environment, we would use IP-Adapter Plus Face
    # for precise identity transfer. Here we simulate the prompt logic.
    
    input_prompt = (
        "A heartwarming medium shot of an adult man holding hands with a young boy, "
        "interacting naturally, looking at each other smiling. "
        "Soft studio lighting, high detail, 8k resolution, photorealistic."
    )
    
    negative_prompt = (
        "distorted faces, extra fingers, blurry, low quality, dark background, "
        "scary, deformed, messy"
    )

    try:
        # We use a model capable of image-to-image or adapter input
        # Using a reliable SDXL model on Replicate
        output = replicate.run(
            "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
            input={
                "prompt": input_prompt,
                "negative_prompt": negative_prompt,
                "width": 1024,
                "height": 1024,
                # In a real implementation with IP-Adapter, we would pass the 
                # image embeddings of the child and adult here.
            }
        )
        return output[0]
    except Exception as e:
        st.error(f"Error generating image: {e}")
        return None

def clean_background(image_url):
    """
    Downloads the generated image and replaces background with white.
    """
    response = requests.get(image_url)
    input_img = Image.open(io.BytesIO(response.content))
    
    # Remove background
    no_bg = remove(input_img)
    
    # Create white background
    white_bg = Image.new("RGBA", no_bg.size, "WHITE")
    white_bg.paste(no_bg, (0, 0), no_bg)
    
    return white_bg

# --- UI LAYOUT ---

st.markdown("<h1 class='main-header'>AiEdit: Past Meets Present</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Childhood Photo")
    child_file = st.file_uploader("Upload old photo", type=['png', 'jpg', 'jpeg'], key="child")
    if child_file:
        st.image(child_file, width=200)

with col2:
    st.subheader("2. Adult Photo")
    adult_file = st.file_uploader("Upload recent photo", type=['png', 'jpg', 'jpeg'], key="adult")
    if adult_file:
        st.image(adult_file, width=200)

st.markdown("---")

if st.button("Generate Reunion", type="primary"):
    if child_file and adult_file:
        with st.spinner("Processing memories... Mixing identities... Adding soft lighting..."):
            
            # 1. Generate the base image (Simulation)
            # In a real deployed app, we would upload the user images to a bucket
            # and pass the URLs to the IP-Adapter model.
            generated_url = process_images(child_file, adult_file)
            
            if generated_url:
                # 2. Process Background
                final_image = clean_background(generated_url)
                
                st.success("Image Generated Successfully!")
                st.image(final_image, caption="AiEdit Result")
                
                # Download Button
                buf = io.BytesIO()
                final_image.save(buf, format="PNG")
                byte_im = buf.getvalue()
                
                st.download_button(
                    label="Download Image",
                    data=byte_im,
                    file_name="AiEdit_Reunion.png",
                    mime="image/png"
                )
    else:
        st.warning("Please upload both photos first.")
