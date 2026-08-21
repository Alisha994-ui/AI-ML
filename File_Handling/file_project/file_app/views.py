from django.shortcuts import render
from django.http import JsonResponse
import os
import pdfplumber
from docx import Document

def uploadpage(request):
    return render(request, "files.html")


def file_upload(request):
    if request.method == "POST":
        file = request.FILES.get("resume")
        folder_path = "uploaded_resume"

        error = validate_file(file,folder_path)
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

        text=text_extract(file_path)
        data=analyze_text(text)

        return JsonResponse({
            "message": "Resume uploaded successfully!",
            "data":data
        }, status=200)

    return JsonResponse({
        "error": "Only POST method is allowed"
    }, status=405)

def validate_file(file,upload_folder):

    if not file:
        return "No file uploaded"

    if not file.name.endswith((".pdf", ".docx")):
        return "Only .pdf and .docx files are allowed"

    if not os.path.exists(upload_folder):
         return  "Upload folder doesn't exist"
                
    return None

def text_extract(uploaded_file):
    text = ""

    if uploaded_file.endswith(".pdf"):

        file = open(uploaded_file, "rb")
        reader = pdfplumber.open(file)

        for page in reader.pages:
            print(page.extract_text())
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
            else:
                text = "No extractable text found on this page."
        file.close()

    else:
        file = Document(uploaded_file)
        for para in file.paragraphs:
            page_text = para.text
            if page_text:
                text += page_text + "\n"
            else:
                text = "No extractable text found in this paragraph."

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