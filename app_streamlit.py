import os
# ✅ Add Tesseract to PATH so Streamlit can find it
os.environ["PATH"] += os.pathsep + r"C:\Program Files\Tesseract-OCR"

import streamlit as st
import spacy
from PIL import Image
import pytesseract

# ✅ Explicitly tell pytesseract where tesseract.exe is
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load SpaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Streamlit UI
st.set_page_config(page_title="AI Answer Sheet Evaluator with OCR", page_icon="🧠", layout="centered")

st.title("🧠 AI Answer Sheet Evaluator with OCR")

# Upload section
uploaded_file = st.file_uploader("Upload student's answer sheet image", type=["jpg", "jpeg", "png"])

# Reference (correct) answer
reference_answer = st.text_area("Reference (Correct) Answer:")

# Evaluate button
if st.button("Evaluate"):
    if not uploaded_file:
        st.warning("⚠️ Please upload a student's answer sheet image.")
    elif not reference_answer.strip():
        st.warning("⚠️ Please enter the reference answer.")
    else:
        # Step 1: Read the image
        image = Image.open(uploaded_file)

        # Step 2: Extract text using OCR
        try:
            student_answer = pytesseract.image_to_string(image)
        except pytesseract.TesseractNotFoundError:
            st.error("❌ Tesseract not found. Please check if it is installed correctly.")
            st.stop()

        # Display extracted text
        st.subheader("📝 Extracted Student Answer:")
        st.write(student_answer.strip() if student_answer.strip() else "No readable text found.")

        # Step 3: Compare with reference answer
        doc1 = nlp(reference_answer)
        doc2 = nlp(student_answer)
        similarity = doc1.similarity(doc2)
        accuracy = round(similarity * 100, 2)

        # Step 4: Display results
        st.subheader("🎯 Evaluation Result")
        st.write(f"Similarity Score: **{accuracy}%**")

        if accuracy > 85:
            grade = "Excellent ✅"
        elif accuracy > 70:
            grade = "Good 🟡"
        elif accuracy > 50:
            grade = "Average ⚪"
        else:
            grade = "Needs Improvement ❌"

        st.write(f"Performance: **{grade}**")

# Optional: Add a small OCR test section
st.divider()
st.caption("🧩 Test OCR Functionality")
test_img = st.file_uploader("Upload any image to test OCR:", type=["jpg", "jpeg", "png"], key="test")
if test_img:
    img = Image.open(test_img)
    st.image(img, caption="Uploaded Image", use_container_width=True)
    text = pytesseract.image_to_string(img)
    st.text_area("Extracted Text:", text)
