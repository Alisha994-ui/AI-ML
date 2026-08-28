# AI-Powered Resume Analyzer

An AI/NLP-based Resume Analyzer built with **Python, Django, Django REST Framework, spaCy, NLTK, and scikit-learn**.

The system allows users to upload resumes in **PDF or DOCX format**, extracts and preprocesses the resume text, detects technical skills and keywords, calculates a resume score, generates feedback, and compares multiple resumes against a given Job Description (JD).

## Features

* PDF and DOCX resume upload
* File format validation
* Resume text extraction
* Text preprocessing and cleaning
* Technical skill detection
* Keyword detection
* Named Entity Recognition (NER) using spaCy
* Resume scoring system
* Experience-based scoring
* Missing skill detection
* Feedback generation
* Job Description matching
* TF-IDF vectorization
* Cosine similarity
* Match percentage calculation
* Multiple resume ranking
* Best resume identification
* JWT authentication
* Django REST Framework API

## Technologies Used

* Python
* Django
* Django REST Framework
* spaCy
* NLTK
* scikit-learn
* pdfplumber
* python-docx
* JWT Authentication
* HTML
* CSS
* JavaScript

## Project Workflow

The system follows this workflow:

```text
Resume Upload
      ↓
File Validation
      ↓
PDF/DOCX Text Extraction
      ↓
Text Preprocessing
      ↓
Skill Detection
      ↓
Keyword Detection
      ↓
Experience Detection
      ↓
NER
      ↓
Resume Scoring
      ↓
Feedback Generation
      ↓
Job Description
      ↓
TF-IDF
      ↓
Cosine Similarity
      ↓
Match Percentage
      ↓
Resume Ranking
```

## 1. File Handling

The system accepts resume files in:

* PDF
* DOCX

Other file types are rejected.

Example:

```text
resume.pdf     ✓ Accepted
resume.docx    ✓ Accepted
resume.jpg     ✗ Rejected
resume.exe     ✗ Rejected
```

The upload endpoint validates the file extension before processing it.

The system also handles missing files and returns a clear error message.

Example:

```json
{
    "error": "Please upload a resume."
}
```

## 2. Text Extraction

The system extracts raw text from uploaded resumes.

### PDF

PDF text is extracted using `pdfplumber`.

### DOCX

DOCX text is extracted using `python-docx`.

The extracted text is then used for NLP processing and scoring.

The system also handles PDFs where text cannot be extracted, such as scanned/image-based PDFs.

## 3. Text Preprocessing

The extracted resume text is cleaned before analysis.

The preprocessing includes:

* Lowercasing
* Whitespace normalization
* Punctuation removal
* Tokenization
* Stopword removal
* Stemming/Lemmatization

For example:

```text
Original:
Experienced Python Developer with Django and SQL.

Cleaned:
experienced python developer django sql
```

This makes the resume text easier to analyze.

## 4. Skill & Keyword Detection

A predefined list of technical skills is used to detect skills in resumes.

Example skills include:

```text
Python
Java
JavaScript
C++
C#
Django
Flask
React
Next.js
Node.js
HTML
CSS
SQL
MySQL
PostgreSQL
MongoDB
Git
Docker
Kubernetes
Jenkins
AWS
Linux
Bash
Ansible
TensorFlow
PyTorch
OpenCV
Machine Learning
```

The matching is:

* Case-insensitive
* Based on whole-word matching
* Designed to avoid partial matches

For example:

```text
Java
```

should not incorrectly match:

```text
JavaScript
```

The system returns detected skills as a clean list.

## 5. Named Entity Recognition

spaCy NER is used to detect entities from resume text.

The system can identify entities such as:

* Organizations
* People
* Dates
* Locations
* Other recognized entities

Example output:

```json
[
    {
        "text": "Google",
        "label": "ORG"
    },
    {
        "text": "2024",
        "label": "DATE"
    }
]
```

## 6. Resume Scoring System

Each resume receives a score out of 100.

The scoring rubric is:

| Category   |   Weight |
| ---------- | -------: |
| Skills     |      40% |
| Keywords   |      30% |
| Experience |      30% |
| **Total**  | **100%** |

The final score is calculated as:

```text
Final Score =
(Skills Score × 0.40)
+
(Keywords Score × 0.30)
+
(Experience Score × 0.30)
```

Example:

```text
Skills Score      = 80
Keywords Score    = 70
Experience Score  = 90

Final Score =
80 × 0.40 +
70 × 0.30 +
90 × 0.30

Final Score = 80
```

The final score is rounded and kept within the 0–100 scoring range.

## 7. Experience Scoring

The system searches resume text for experience information such as:

```text
2 years experience
3 years of experience
6 months experience
```

The detected experience is converted into an experience score.

This score contributes 30% to the final resume score.

## 8. Suggestions for Improvement

The analyzer identifies weak areas in a resume.

It can generate suggestions related to:

* Missing skills
* Weak experience
* Missing keywords
* Other scoring weaknesses

Example:

```text
Add more project experience.
```

or:

```text
Consider adding Python and Django to your resume.
```

Suggestions are returned as a list so they can easily be displayed by the frontend.

## 9. Job Description Matching

The system accepts a Job Description as plain text.

Example:

```text
We are looking for a Python Django Developer
with experience in REST APIs, PostgreSQL,
Git and Docker.
```

The Job Description is compared with every uploaded resume.

## 10. TF-IDF

The system uses **TF-IDF (Term Frequency–Inverse Document Frequency)** to convert the Job Description and resumes into numerical vectors.

The documents are combined:

```python
texts = [job_description] + resume_texts
```

Then:

```python
vectorizer = TfidfVectorizer(
    stop_words="english"
)

vectors = vectorizer.fit_transform(texts)
```

TF-IDF gives more importance to words that are useful for distinguishing documents.

Common English stopwords are ignored.

## 11. Cosine Similarity

After TF-IDF vectorization, cosine similarity is used to compare the Job Description with each resume.

```python
similarity = cosine_similarity(
    job_vector,
    resume_vector
)[0][0]
```

The similarity value ranges approximately from:

```text
0 → No similarity
1 → Very high similarity
```

It is converted into a percentage:

```python
similarity_score = round(
    similarity * 100,
    2
)
```

Example:

```text
Cosine Similarity = 0.82

Match Percentage = 82%
```

## 12. Ranking Multiple Resumes

The system can process multiple uploaded resumes against one Job Description.

For each resume it calculates:

* Final Score
* JD Similarity
* Match Percentage

The results are then sorted from highest to lowest similarity.

Example:

| Rank | Name      | Score | Match % |
| ---: | --------- | ----: | ------: |
|    1 | Ali.pdf   |    88 |     92% |
|    2 | Sara.pdf  |    82 |     85% |
|    3 | Ahmed.pdf |    76 |     79% |
|    4 | Hamza.pdf |    70 |     68% |
|    5 | Usman.pdf |    63 |     61% |

The highest matching resume is displayed as the **Best Resume**.

## 13. Batch Processing

Multiple resumes can be processed in a single analysis request.

The system loops through all valid resumes:

```python
for index, resume in enumerate(valid_resumes):
```

Each resume is processed independently.

If one resume cannot be read, the error is handled and processing can continue for the remaining resumes.

## 14. API Endpoints

### Login Page

```text
/login/
```

### Resume Upload

```text
POST /api/resumes/
```

### Current User

```text
GET /api/me/
```

### Resume Analysis

```text
POST /api/resumes/analyze/
```

The Job Description is sent as:

```json
{
    "job_description": "Python Django Developer with REST API and PostgreSQL experience"
}
```

The analysis response contains the ranked resumes.

Example:

```json
{
    "message": "Job description analyzed successfully.",
    "job_description": "Python Django Developer...",
    "resumes": [
        {
            "file": "resume1.pdf",
            "final_score": 88,
            "similarity_score": 92
        }
    ]
}
```

## 15. Authentication

JWT authentication is used to protect API endpoints.

The frontend stores the access token and sends it with API requests:

```text
Authorization: Bearer <access_token>
```

Admin-only operations are protected using:

```python
IsAdminUser
```

Authenticated operations use:

```python
IsAuthenticated
```

## 16. Error Handling

The system handles common errors such as:

### No file

```json
{
    "error": "Please upload a resume."
}
```

### Unsupported file

```json
{
    "error": "Only PDF and DOCX files are allowed."
}
```

### Empty Job Description

```json
{
    "error": "Job description is required."
}
```

### No resumes

```json
{
    "error": "No resumes available."
}
```

### Unreadable resumes

Unreadable files are skipped during batch processing so that one broken file does not stop the complete analysis.

## 17. Sample Dataset

For testing, a small dataset of 5–10 template/anonymized resumes can be used.

Example:

```text
dataset/
├── resume_01.pdf
├── resume_02.pdf
├── resume_03.pdf
├── resume_04.docx
├── resume_05.pdf
└── resume_06.docx
```

The resumes should contain different combinations of:

* Skills
* Keywords
* Experience
* Projects
* Education

This allows the scoring and ranking system to be tested with different candidates.

## 18. Testing

The system should be tested using:

### Valid files

```text
resume.pdf
resume.docx
```

### Invalid files

```text
image.jpg
program.exe
document.txt
```

### Edge cases

* Empty file
* Empty Job Description
* Scanned PDF
* Corrupted PDF
* Corrupted DOCX
* Resume with no technical skills
* Resume with no experience
* Multiple resumes with similar scores

## 19. Expected Output

After entering a Job Description, the application displays a ranking table:

```text
Resume Ranking

Rank    Name             Score       Match %
------------------------------------------------
🥇 1    resume_03.pdf     91          94%
🥈 2    resume_01.pdf     86          88%
🥉 3    resume_05.pdf     79          81%
   4    resume_02.pdf     73          75%
   5    resume_04.docx    65          68%
```

The highest-ranked resume is also displayed separately as the Best Resume.

## 20. Project Structure

A simplified project structure:

```text
resume_analyzer/
│
├── manage.py
│
├── project/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── resume_app/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   │
│   ├── utils/
│   │   ├── file_processing.py
│   │   └── feedback_Section.py
│   │
│   └── templates/
│       ├── login.html
│       ├── files.html
│       └── resumes.html
│
└── dataset/
    ├── resume_01.pdf
    ├── resume_02.pdf
    └── ...
```

## 21. Installation

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install django djangorestframework spacy scikit-learn pdfplumber python-docx nltk
```

Install the spaCy English model:

```bash
python -m spacy download en_core_web_sm
```

Run migrations:

```bash
python manage.py migrate
```

Start the development server:

```bash
python manage.py runserver
```

Open the application:

```text
http://127.0.0.1:8000/login/
```

## 22. Scoring Explanation

The analyzer uses two different types of scoring.

### Resume Score

The general resume score is based on:

```text
Skills       → 40%
Keywords     → 30%
Experience   → 30%
```

### JD Match

The JD Match percentage is calculated separately using:

```text
TF-IDF + Cosine Similarity
```

Therefore:

```text
Final Score
```

and

```text
JD Match %
```

represent different measurements.

A resume can have a high general score but a lower JD match if its skills do not closely match the specific Job Description.

## 23. Stage 4 Tasks Completed

### File Handling

* PDF/DOCX validation
* Unsupported file rejection
* File existence/error handling
* Reusable file processing
* Django upload endpoint

### Text Extraction

* PDF text extraction
* DOCX text extraction
* Character/word analysis
* Scanned PDF handling
* Common extraction function

### NLP Preprocessing

* Lowercasing
* Whitespace normalization
* Punctuation removal
* Tokenization
* Stopword removal
* Lemmatization/stemming

### Skill & Keyword Detection

* Predefined skill list
* Skill matching
* Case-insensitive matching
* Whole-word matching
* spaCy NER
* Clean skill lists

### Resume Scoring

* Weighted scoring rubric
* Skill scoring
* Experience scoring
* Score normalization
* 0–100 score
* Multiple resume testing

### Suggestions

* Missing skills
* Weak area detection
* Missing keyword suggestions
* Actionable feedback
* List-based suggestions

### Job Description Matching

* JD input
* JD/resume comparison
* TF-IDF
* Cosine similarity
* Match percentage

### Multiple Resume Ranking

* Batch processing
* Sorting
* Ranking
* Comparative scoring
* Best resume selection
* Ranking table
* Broken-file handling

## 24. Future Improvements

Possible improvements include:

* Better resume section detection
* More accurate experience extraction
* Advanced skill extraction using NLP
* Semantic similarity using transformer models
* Job-specific scoring weights
* Resume recommendations
* Recruiter dashboard
* Export ranking results to CSV/PDF
* More detailed candidate comparison

## Conclusion

The AI-Powered Resume Analyzer demonstrates an end-to-end NLP pipeline for resume processing and Job Description matching. It combines traditional text processing, rule-based skill detection, scoring logic, spaCy NER, TF-IDF, cosine similarity, and multi-resume ranking to help identify resumes that are most relevant to a specific job description.
