import streamlit as st
import requests
from pdf2image import convert_from_bytes
import ast
import time
import http.client
import json
def process_api_response(response_text):
    # Remove the initial query portion.
    # Assume the answer portion starts at the first header "###"
    start_index = response_text.find("###")
    if start_index != -1:
        answer_text = response_text[start_index:]
    else:
        answer_text = response_text

    # Option 1: Replace newlines with spaces
    # This will produce one long line.
    cleaned_text = answer_text.replace("\n", "")
    cleaned_text = cleaned_text.replace('{"result":"', "").replace('","status":true}', "")
    
    # Remove the trailing query and unnecessary parts
    cleaned_text = cleaned_text.replace("Do you have any other questions or would you like me to elaborate on any of these conditions?", "")
    
    # Option 2: Split into sections (if you prefer a list)
    # sections = [line.strip() for line in answer_text.split("###") if line.strip()]
    # You could then join them with bullet points, for example:
    # cleaned_text = "\n".join(f"• {section}" for section in sections)

    # Remove extra spaces
    cleaned_text = " ".join(cleaned_text.split())
    return cleaned_text



# Function to call the ChatGPT API using RapidAPI
def get_diseases_from_symptoms(symptoms):
    conn = http.client.HTTPSConnection("open-ai21.p.rapidapi.com")
    # Build the query dynamically from the extracted condition (symptoms)
    if file_format == "prescription":
        query = f"Can you tell me these are the symptoms of which diseases: {input_text}"
    elif file_format == "patient_details":
        query = f"What could be the effect of this disease and how to cure it: {input_text}"
    else:
        query = "Provide relevant medical information."
    payload_dict = {
        "messages": [
            {
                "role": "user",
                "content": query
            }
        ],
        "web_access": False
    }
    payload = json.dumps(payload_dict)
    headers = {
        'x-rapidapi-key': "9e8a2e21dfmshcc3d1f45e62e3b9p1e0b7djsna1c0f8d687e8",
        'x-rapidapi-host': "open-ai21.p.rapidapi.com",
        'Content-Type': "application/json"
    }
    conn.request("POST", "/conversationllama", payload, headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")

# Define paths and backend URL
POPPLER_PATH = r"C:\poppler-24.02.0\poppler-24.08.0\Library\bin"
URL = "http://127.0.0.1:9000/extract_from_doc"
st.markdown(
    """
    <style>
    body, .stApp {
          background: linear-gradient(135deg, #e3f2fd, #bbdefb); /* Soft blue gradient */
        color: #333; /* Dark text */
        font-family: 'Arial', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <h1 style='
    text-align: center; 
               font-size: 42px;'>
        🏥 Smart Prescription Reader
    </h1>
    """,
    unsafe_allow_html=True
)


file = st.file_uploader("Upload file", type="pdf")
col3, col4 = st.columns(2)
with col3:
    file_format = st.radio(label="Select type of document", options=["prescription", "patient_details"], horizontal=True)
with col4:
    if file and st.button("Upload PDF", type="primary"):
        bar = st.progress(50)
        time.sleep(3)
        bar.progress(100)
        payload = {'file_format': file_format}
        files = [('file', file.getvalue())]
        headers = {}
        response = requests.request("POST", URL, headers=headers, data=payload, files=files)
        dict_str = response.content.decode("UTF-8")  # Get response as a string

        # Debugging: Check raw API response
        print("Raw API Response:", repr(dict_str))  
        
        # Convert API response safely
        try:
            data = json.loads(dict_str)  # Use json.loads() instead of ast.literal_eval()
            print("Parsed Data:", data)  # Debugging line
        except json.JSONDecodeError as e:
            print("JSON Parsing Error:", e)
            data = {}  # Set empty dict to prevent errors later
        
        # Store the parsed data in session state if valid
        if data:
            st.session_state = data


if file:
    pages = convert_from_bytes(file.getvalue(), poppler_path=POPPLER_PATH)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Your file")
        st.image(pages[0])
    with col2:
        if st.session_state:
            st.subheader("Details")
            if file_format == "prescription":
                name = st.text_input(label="Name", value=st.session_state.get("patient_name", ""))
                address = st.text_input(label="Address", value=st.session_state.get("patient_address", ""))
                condition = st.text_input(label="Condition", value=st.session_state.get("condition", ""))
                medicines = st.text_area(label="Medicines", value=st.session_state.get("medicines", ""))
                directions = st.text_input(label="Directions", value=st.session_state.get("directions", ""))
                refill = st.text_input(label="Refill", value=st.session_state.get("refill", ""))
            if file_format == "patient_details":
                name = st.text_input(label="Name", value=st.session_state.get("patient_name", ""))
                phone = st.text_input(label="Phone No.", value=st.session_state.get("phone_no", ""))
                vacc_status = st.text_input(label="Hepatitis B vaccination status", value=st.session_state.get("vaccination_status", ""))
                med_problems = st.text_input(label="Medical Problems", value=st.session_state.get("medical_problems", ""))
                has_insurance = st.text_input(label="Does patient have taken insurance?", value=st.session_state.get("has_insurance", ""))
            
            # When the user clicks Submit, call the ChatGPT API with the condition (symptoms)
            if st.button("Submit", type="primary"):
               if file_format == "prescription":
                 
                 input_text = st.session_state.get("condition", "")
                
               elif file_format == "patient_details":
                 input_text = st.session_state.get("medical_problems", "")
               if input_text:
                   chatgpt_response = get_diseases_from_symptoms(input_text)
                   processed_response = process_api_response(chatgpt_response)
                   st.subheader("Diseases based on symptoms")
                   st.markdown(
    f"""
    <div style='margin-left: 0;'>
    <div style='width: 40vw; max-width: 1200px; white-space: pre-line; font-size:16px; line-height:1.8; padding:10px; border:1px solid #ddd; border-radius:5px; background-color:#f9f9f9;'>
        {processed_response}
    </div>
     </div>
    """,
    unsafe_allow_html=True
)
               else:
                   st.error("Condition is empty. Please provide symptoms.")
               for key in list(st.session_state.keys()):
                   del st.session_state[key]
               st.success('Details successfully recorded.')
