import os
import streamlit as st
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_host = os.environ.get("HOST", "api")
api_port = int(os.environ.get("PORT", 8080))


# Streamlit UI elements
st.title("Mock Interview Simulator")

with st.sidebar:
    st.markdown(
        "## How to use\n"
        "1. Add your resume\n"
        "2. Add the company information / Code of conduct / roles and responsibilty etc.\n"
        "3. Select interview type\n"
        "4. Ask to conduct a Mock Interview"
    )
    st.markdown(
        "The development of this app and required pipelines is still under progress. hoping to finsih it soon. First time handling open source project... Thanks for understanding :)\n"

    )

question = st.text_input(
    "Search for something",
    placeholder="type: simulate an interview for me"
)
# File Upload
resume_file = st.file_uploader("Upload Your Resume (PDF)", type=["pdf"])
company_info_file = st.file_uploader("Upload Company Info (PDF)", type=["pdf"])

# Domain Selection
domain = st.selectbox("Select Interview Domain", ["Software", "Technical", "HR", "Mangement"])


if question:
    url = f'http://{api_host}:{api_port}/'
    data = {"query": question}
    print(f'Url: {url}')

    response = requests.post(url, json=data)

    if response.status_code == 200:
        st.write("### Answer")
        st.write(response.json())
    else:
        st.error(f"Failed to send data to Pathway API. Status code: {response.status_code}")
