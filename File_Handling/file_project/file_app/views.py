from django.shortcuts import render
from django.http import JsonResponse
import os
import pdfplumber
from docx import Document

import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer


nltk.download("stopwords")
nltk.download("punkt_tab")


def uploadpage(request):
    return render(request, "files.html")


def file_upload(request):

    if request.method == "POST":
        file = request.FILES.get("resume")
        folder_path = "uploaded_resume"
        error = validate_file(file, folder_path)

        if error:
            return JsonResponse({
                "error": error
            }, status=400)

        file_path = os.path.join(folder_path, file.name)
        with open(file_path, "wb") as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        if not os.path.exists(file_path):
            return JsonResponse({
                "error": "File path doesn't exist"
            }, status=400)

        text = text_extract(file_path)
        data = analyze_text(text)

        #Section 3
        original_data = "ALISHA is learning Python, and she is playing games!!!"
        preprocessing_data = text_preprocessing(original_data)
        create_report(original_data, preprocessing_data)

        return JsonResponse({
            "message": "Resume uploaded successfully!",
            "data": data,
            "preprocessing": preprocessing_data
        }, status=200)

    return JsonResponse({
        "error": "Only POST method is allowed"
    }, status=405)


def validate_file(file, upload_folder):

    if not file:
        return "No file uploaded"
    if not file.name.endswith((".pdf", ".docx")):
        return "Only .pdf and .docx files are allowed"
    if not os.path.exists(upload_folder):
        return "Upload folder doesn't exist"
    return None


def text_extract(uploaded_file):
    text = ""

    if uploaded_file.endswith(".pdf"):
        file = open(uploaded_file, "rb")
        reader = pdfplumber.open(file)

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
            else:
                print("No extractable text found on this page.")

        file.close()
    else:
        file = Document(uploaded_file)
        for para in file.paragraphs:
            page_text = para.text
            if page_text:
                text += page_text + "\n"
            else:
                print("No extractable text found in this paragraph.")
    return text


def analyze_text(text):

    text = text.replace("(cid:127)", "•")
    words = text.split()
    words_count = len(words)
    char_count = len(text)
    data = {
        "text": text,
        "words_count": words_count,
        "char_count": char_count
    }
    return data

def text_preprocessing(text):

    # Lowercasing
    lower_text = text.lower()

    # Whitespace normalization
    whitespace_text = " ".join(lower_text.split())

    # Punctuation removal
    punct_text = whitespace_text.translate(
        str.maketrans("", "", string.punctuation)
    )

    # Tokenization
    tokens = word_tokenize(punct_text)

    # Stopwords removal
    stop_words_list = set(stopwords.words("english"))
    clean = []
    for token in tokens:
        if token not in stop_words_list:
            clean.append(token)

    # Stemming
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


def create_report(data, preprocessing_data):

    file_path = "text_processing.txt"
    with open(file_path, "w", encoding="utf-8") as file:
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