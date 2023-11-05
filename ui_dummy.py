import streamlit as st
import requests

st.title("Mock Interview Simulator App")

# File Upload
resume_file = st.file_uploader("Upload Your Resume (PDF)", type=["pdf"])
company_info_file = st.file_uploader("Upload Company Info (PDF)", type=["pdf"])

# Domain Selection
domain = st.selectbox("Select Interview Domain", ["Software", "Technical"])

if st.button("Start Mock Interview"):
    if resume_file is not None and company_info_file is not None:
        # Process uploaded files
        # You can use the uploaded files as needed, e.g., save to the 'uploads/' directory.
        
        
        # Initialize your Pathway API endpoint and provide necessary authentication
        pathway_api_url = "YOUR_PATHWAY_API_ENDPOINT"
        api_key = "YOUR_API_KEY"

        # Construct the request data
        data = {
            "resume_pdf": resume_file.read(),
            "company_info_pdf": company_info_file.read(),
            "domain": domain,
        }

        headers = {
            "Authorization": f"Bearer {api_key}"
        }

        # Send the POST request to the Pathway API
        response = requests.post(pathway_api_url, json=data, headers=headers)

        if response.status_code == 200:
            st.write("### Answer")
            st.write(response.json())
        else:
            st.error(f"Failed to send data to Pathway API. Status code: {response.status_code}")
    else:
        st.warning("Please upload both your resume and company information PDFs.")
