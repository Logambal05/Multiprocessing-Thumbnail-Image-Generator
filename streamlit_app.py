import os
import shutil
import subprocess
import streamlit as st

st.set_page_config(
    page_title="Thumbnail Generator",
    layout="wide",
    initial_sidebar_state="expanded"
)

PRODUCER_DIR = "producer"
CONSUMER_DIR = "consumer"
SAMPLE_DIR = "assets"

st.title("Thumbnail Generator with Multiprocessing")

for folder in [PRODUCER_DIR, CONSUMER_DIR]:
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder)

tab1, tab2 = st.tabs(["Upload Images", "Use Sample Images"])

with tab1:
    uploaded_files = st.file_uploader("Upload images", type=["jpg", "png"], accept_multiple_files=True)
    if uploaded_files:
        for file in uploaded_files:
            with open(os.path.join(PRODUCER_DIR, file.name), "wb") as f:
                f.write(file.getbuffer())
        st.success(f"{len(uploaded_files)} Images uploaded!")

    if st.button("Generate Thumbnails"):
        with st.spinner("Processing thumbnails"):
            subprocess.run(["python3", "producer_consumer.py"])
        st.info(f"{len(uploaded_files)} Thumbnail Image Generated!")

        thumbnails = os.listdir(CONSUMER_DIR)
        for thumb in thumbnails:
            path = os.path.join(CONSUMER_DIR, thumb)
            st.image(path, caption=thumb, width=150)
            with open(path, "rb") as f:
                st.download_button("Download " + thumb, data=f, file_name=thumb, mime="image/jpeg")

with tab2:
    sample_images = os.listdir(SAMPLE_DIR)
    if sample_images:
        selected = st.multiselect("Select sample images to process", sample_images)

        if selected:
            for img in selected:
                shutil.copy2(os.path.join(SAMPLE_DIR, img), PRODUCER_DIR)
            st.success(f"{len(selected)} sample image(s) selected!")

        if st.button("Generate Thumbnails (Sample Images)"):
            with st.spinner("Processing thumbnails..."):
                subprocess.run(["python3", "producer_consumer.py"])
            st.success(f"{len(selected)} Thumbnail Image Generated!")

            thumbnails = os.listdir(CONSUMER_DIR)
            for thumb in thumbnails:
                path = os.path.join(CONSUMER_DIR, thumb)
                st.image(path, caption=thumb, width=150)
                with open(path, "rb") as f:
                    st.download_button("Download " + thumb, data=f, file_name=thumb, mime="image/jpeg")
    else:
        st.info("No sample images found in the 'assets' folder.")
