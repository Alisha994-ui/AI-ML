import pdfplumber
from docx import Document
import re
import string
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

def validate_file(file, upload_folder):
    if not file:
        return "No file uploaded"

    if not file.name.lower().endswith((".pdf", ".docx")):
        return "Only .pdf and .docx files are allowed"

    os.makedirs(upload_folder, exist_ok=True)

    return None

def text_extract(uploaded_file):
    extracted_text = ""

    if uploaded_file.lower().endswith(".pdf"):
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text(
                    x_tolerance=2,
                    y_tolerance=3
                )
                if page_text:
                    extracted_text += page_text + "\n"

    elif uploaded_file.lower().endswith(".docx"):
        document = Document(uploaded_file)
        for paragraph in document.paragraphs:
            extracted_text += paragraph.text + "\n"
    return extracted_text

def analyze_text(text):
    text = text.replace("(cid:127)","•")
    words = text.split()
    words_count = len(words)
    char_count = len(text)
    data = {"text": text,"words_count": words_count,"char_count": char_count}
    return data

def text_preprocessing(text):
    lower_text = text.lower()
    whitespace_text = " ".join(lower_text.split())

    punct_text = whitespace_text.translate(
        str.maketrans("","",string.punctuation))

    tokens = word_tokenize(punct_text)

    stop_words_list = set(stopwords.words("english"))

    clean = []
    for token in tokens:
        if token not in stop_words_list:
            clean.append(token)

    stemmer = PorterStemmer()
    stemmed_words = []
    for word in clean:
        stemmed_words.append(stemmer.stem(word))

    return {
        "lowercase": lower_text,
        "whitespace_text": whitespace_text,
        "punct_text": punct_text,
        "tokens": tokens,
        "without_stopwords": clean,
        "stemmed_words": stemmed_words
    }
def create_report(data,preprocessing_data):
    file_path = "text_processing.txt"
    with open(file_path,"w",encoding="utf-8") as file:
        file.write("========== TEXT ANALYSIS ==========\n\n")
        file.write("Original Text:\n")
        file.write(data)
        file.write("\n\n")
        file.write("========== TEXT PREPROCESSING ==========\n\n")
        file.write("After Lowercasing:\n")
        file.write(preprocessing_data["lowercase"])
        file.write("\n\n")
        file.write("After Whitespace Normalization:\n")
        file.write(preprocessing_data["whitespace_text"])
        file.write("\n\n")
        file.write("After Punctuation Removal:\n")
        file.write(preprocessing_data["punct_text"])
        file.write("\n\n")
        file.write("Tokens:\n")
        file.write(str(preprocessing_data["tokens"]))
        file.write("\n\n")
        file.write("After Stopwords Removal:\n")
        file.write(str(preprocessing_data["without_stopwords"]))
        file.write("\n\n")
        file.write("After Stemming:\n")
        file.write(str(preprocessing_data["stemmed_words"]))
        file.write("\n")

tech_skills={
    "python":10,
    "java":5,
    "javascript":5,
    "c++":5,
    "c#":5,
    "php":5,
    "django":10,
    "flask":5,
    "react":5,
    "next.js":10,
    "node.js":10,
    "html":5,
    "css":5,
    "sql":10,
    "mysql":5
}

def extract_skills(text):
    missing_skills=[]
    found_skills=[]
    text=text.lower()
    for skill in tech_skills:
        pattern=r"(?<!\w)"+re.escape(skill)+r"(?!\w)"
        if re.search(pattern,text):
            found_skills.append(skill)
        else:
            missing_skills.append(skill)
    return missing_skills,found_skills

def calculate_score(matched_skills):
    total_score=sum(tech_skills.values())
    score=0
    for skill in set(matched_skills):
        if skill in tech_skills:
            score+=tech_skills[skill]
    if total_score==0:
        return 0
    score_out_of_100=(score/total_score)*100
    return round(score_out_of_100,2)

job_keywords=[
    "rest api",
    "restful api",
    "ci/cd",
    "deployment",
    "debugging",
    "problem solving",
    "team collaboration",
    "agile",
    "database",
    "testing"
]

def calculate_keyword_score(text):
    text=text.lower()
    missing_keywords=[]
    matched_keywords=[]
    for keyword in job_keywords:
        pattern=r"(?<!\w)"+re.escape(keyword)+r"(?!\w)"
        if re.search(pattern,text):
            matched_keywords.append(keyword)
        else:
            missing_keywords.append(keyword)
    if len(job_keywords)==0:
        return 0,matched_keywords,missing_keywords
    score=(len(matched_keywords)/len(job_keywords))*100
    return round(score,2),matched_keywords,missing_keywords

def calculate_experience_score(text):
    text=text.lower()
    year_matches=re.findall(r"\b(\d+(?:\.\d+)?)\s*\+?\s*(years?|yrs?)\b",text)
    if year_matches:
        highest_years=max(float(match[0]) for match in year_matches)
        if highest_years>=2:
            return 100
        elif highest_years>=1:
            return 80
        else:
            return 60
    month_matches=re.findall(r"\b(\d+)\s*\+?\s*(months?|mos?)\b",text)
    if month_matches:
        highest_months=max(int(match[0]) for match in month_matches)
        if highest_months>=12:
            return 80
        elif highest_months>=6:
            return 60
        elif highest_months>0:
            return 40
    experience_words=[
        "intern",
        "internship",
        "experience",
        "developer",
        "engineer"
    ]
    for word in experience_words:
        if re.search(r"(?<!\w)"+re.escape(word)+r"(?!\w)",text):
            return 40
    return 0