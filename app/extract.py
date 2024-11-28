import os
import sqlite3
import pdfplumber
import re

# Paths
pdf_folder = r"D:\Pradeep\cv\2024\inizio\fast_api_py_1\pythonProject\publication"
db_path = r"D:\Pradeep\cv\2024\inizio\fast_api_py_1\pythonProject\psoriasis.db"

# Connect to SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Recreate the `publication` table to ensure fresh data
cursor.execute('DROP TABLE IF EXISTS publication')
cursor.execute('''
    CREATE TABLE publication (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT,
        abstract TEXT,
        content TEXT
    )
''')

# Function to preprocess and normalize text
def preprocess_text(text):
    # Remove extra whitespaces (including new lines and tabs)
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Remove unwanted characters (keep only alphanumeric, spaces, and basic punctuation)
    text = re.sub(r'[^\w\s,.!?;:()-]', '', text)
    
    # Normalize case to lowercase (if needed)
    text = text.lower()
    
    return text

# Function to extract topic, abstract, and content from text
def extract_topic_abstract_content(text):
    lines = text.splitlines()
    topic = None
    abstract = None
    content = None

    # Find "Review", "Abstract", and "Keywords"
    review_index = next((i for i, line in enumerate(lines) if "Review" in line), None)
    abstract_index = next((i for i, line in enumerate(lines) if "Abstract" in line), None)
    keywords_index = next((i for i, line in enumerate(lines) if "Keywords" in line), None)
    
    # Extract the topic (line after "Review")
    if review_index is not None:
        topic = lines[review_index + 1].strip() if review_index + 1 < len(lines) else "Unknown Topic"
    else:
        topic = "Unknown Topic"
    
    # Extract the abstract, preserving spacing and handling same-line content
    if abstract_index is not None:
        abstract_lines = []
        # Handle text directly after "Abstract" on the same line
        abstract_start = lines[abstract_index].split("Abstract", 1)[-1].strip()
        if abstract_start:
            abstract_lines.append(abstract_start)
        # Handle text in subsequent lines until "Keywords"
        if keywords_index is not None:
            abstract_lines.extend(lines[abstract_index + 1:keywords_index])
        else:
            abstract_lines.extend(lines[abstract_index + 1:])  # No "Keywords" found
        abstract = "\n".join(abstract_lines).strip()
    else:
        abstract = "Unknown Abstract"

    # Extract the content (everything before the topic, after the abstract, or outside the abstract section)
    content_lines = lines[:review_index]  # All lines before "Review"
    if keywords_index is not None:
        content_lines.extend(lines[keywords_index + 1:])  # All lines after "Keywords"
    content = "\n".join(content_lines).strip()

    # Preprocess/clean the extracted text
    topic = preprocess_text(topic)
    abstract = preprocess_text(abstract)
    content = preprocess_text(content)

    return topic, abstract, content

# Process only two PDF files
pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
pdf_files = pdf_files[:2]  # Limit to the first two PDF files

for file_name in pdf_files:
    file_path = os.path.join(pdf_folder, file_name)
    print(f"Processing: {file_name}")
    
    # Extract text from the PDF
    content = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                content += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error reading {file_name}: {e}")
        continue

    # Extract topic, abstract, and content
    topic, abstract, extra_content = extract_topic_abstract_content(content)

    # Insert into SQLite
    cursor.execute('''
        INSERT INTO publication (topic, abstract, content)
        VALUES (?, ?, ?)
    ''', (topic, abstract, extra_content))

# Commit changes and close the connection
conn.commit()
conn.close()

print("Topics, abstracts, and content from two PDFs saved to psoriasis.db in the `publication` table.")
