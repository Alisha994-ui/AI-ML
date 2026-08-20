from django.shortcuts import render
from django.http import JsonResponse
import os


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

        return JsonResponse({
            "message": "Resume uploaded successfully!"
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