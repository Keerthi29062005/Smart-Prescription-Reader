# Smart Prescription Reader
A powerful OCR-based project designed to extract critical patient and prescription details from PDF documents. This system includes a backend server that processes data extraction requests efficiently. Additionally, it integrates OpenAI’s API to analyze patient health information, providing valuable insights that can assist medical professionals in diagnosis and treatment.

## Demo

## [Click here to see project presentation](https://drive.google.com/file/d/1ZQQus2-apLWkvz_f2Y-2Sx7I_rxtH7iK/view?usp=drive_link)

## <a name="a1">1. What is OCR?</a>
OCR, or Optical Character Recognition, is a technology that transforms various document types—such as scanned pages, PDFs, and images—into editable and searchable text. By recognizing characters within images or scanned documents, OCR converts them into machine-readable format.  

Artificial intelligence (AI) and machine learning (ML) play a crucial role in enhancing OCR accuracy. ML-driven OCR systems utilize convolutional neural networks (CNNs) trained on vast datasets to identify text within images. These algorithms extract key features and leverage language models to interpret context, reducing errors caused by ambiguous characters. Additionally, OCR systems continuously learn and refine their performance over time, adapting to specific languages and domains for improved recognition accuracy.

## <a name="a2">2. Introduction to Project</a>
In healthcare, vast amounts of medical data are generated from forms, prescriptions, and test reports. These documents help maintain patient records, track medical history, and are often required for processes like health insurance claims.

Health insurance companies receive thousands of such documents daily from multiple sources. Manually extracting key information from these records is time-consuming and requires significant manpower. OCR (Optical Character Recognition) technology can automate and accelerate this process, improving efficiency and accuracy.

In this project, we focus on extracting critical information from two types of medical documents:

Patient Medical Records – Contains details like name, contact information, medical history, and insurance status.
Prescriptions – Includes patient name, prescribed medicines, dosage instructions, refill details, and diagnosed conditions.
Additionally, the system integrates AI-powered analysis to provide insights into patient symptoms and medical conditions, assisting healthcare professionals in decision-making and treatment planning.

## <a name="a8">3. Steps to clone this repository?</a>
- Install all dependancies from `requirements.txt`
- For `pdf2image` you need to [download `poppler`](https://github.com/belval/pdf2image?tab=readme-ov-file#how-to-install)
- Install Tesseract OCR Engine in your PC
    - [Tesseract installation instrution : Github](https://github.com/tesseract-ocr/tesseract#installing-tesseract)
    - [Tesseract windows specific instructions: Github](https://github.com/UB-Mannheim/tesseract/wiki)
- Set required PATHs as per your environment
