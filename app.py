import spacy

# Load English language model
nlp = spacy.load("en_core_web_sm")

print("===========================================")
print("🧠  AI Answer Evaluator")
print("===========================================\n")

# Take input from user
reference_answer = input("Enter the reference (correct) answer:\n> ")
student_answer = input("\nEnter the student's answer:\n> ")

# Process both answers using spaCy
doc1 = nlp(reference_answer)
doc2 = nlp(student_answer)

# Calculate similarity
similarity = doc1.similarity(doc2)

# Convert similarity to percentage
accuracy = round(similarity * 100, 2)

print("\n-------------------------------------------")
print(f"Similarity Score: {accuracy}%")

# Optional grading system
if accuracy > 85:
    grade = "Excellent"
elif accuracy > 70:
    grade = "Good"
elif accuracy > 50:
    grade = "Average"
else:
    grade = "Needs Improvement"

print(f"Performance: {grade}")
print("-------------------------------------------")
