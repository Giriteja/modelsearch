import streamlit as st
from google.cloud import storage
import pydeck as pdk
import streamlit.components.v1 as components
# Set up a GCS client
import os
import subprocess
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "learninpad-dc6bc04e9251.json"

# Function to search for files in a GCS bucket
def search_gcs_bucket(bucket_name, prefix):
    bucket = storage_client = storage.Client().bucket(bucket_name)
    blobs = list(bucket.list_blobs(prefix=prefix))
    return blobs


def read_html_file(path):
    with open(path, 'r') as file:
        return file.read()

# Streamlit app
def main():
    st.title("Google Cloud Storage File Search")
    
    # Sidebar for input
    st.sidebar.header("Search Parameters")
    bucket_name = st.sidebar.text_input("Enter GCS Bucket Name:",value="model_assets_library")
    prefix = st.sidebar.text_input("Enter Prefix (optional):",value="assets/plate_with_ice.glb")

    if st.sidebar.button("Search"):
        if bucket_name:
            st.subheader(f"Search Results in Bucket: {bucket_name}")
            if prefix:
                st.write(f"Searching for files with prefix '{prefix}'")
            else:
                st.write("Searching for all files in the bucket")

            # Search for files in GCS
            blobs = search_gcs_bucket(bucket_name, prefix)

            result = subprocess.run(["gsutil", "ls", f"gs://{bucket_name}/{prefix}"], capture_output=True, text=True, shell=True)
            download_link = f"[Download {prefix}](https://storage.googleapis.com/{bucket_name}/{prefix})"
            st.markdown(download_link, unsafe_allow_html=True)
            html_content = read_html_file("model.html")

            # Use Streamlit components to render the HTML
            components.html(html_content, height=600)
              
        else:
            st.error("Please enter a GCS bucket name to perform the search.")

if __name__ == "__main__":
    main()