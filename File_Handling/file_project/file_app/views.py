from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Resume
from .serializers import ResumeSerializer
from .utils.file_processing import (
    text_extract,
    extract_skills,
    calculate_score,
    calculate_experience_score,
    calculate_keyword_score,
    analyze_text
)
from .utils.feedback_Section import (
    weak_area,
    feedback_generation,
    keywords_suggestion
)

def loginpage(request):
    return render(request, "login.html")

def uploadpage(request):
    return render(request, "files.html")

def resumespage(request):
    return render(request, "resumes.html")

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def current_user(request):
    return Response({
        "username": request.user.username,
        "is_staff": request.user.is_staff,
        "is_superuser": request.user.is_superuser
    })

class ResumeViewSet(ModelViewSet):
    queryset = Resume.objects.all().order_by("-final_score", "-uploaded_at")
    serializer_class = ResumeSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        file = request.FILES.get("file")

        if not file:
            return Response(
                {"error": "Please upload a resume."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not file.name.lower().endswith((".pdf", ".docx")):
            return Response(
                {"error": "Only PDF and DOCX files are allowed."},
                status=status.HTTP_400_BAD_REQUEST
            )

        resume = Resume.objects.create(file=file)

        extracted_text = text_extract(resume.file.path)
        data = analyze_text(extracted_text)

        missing_skills, matched_skills = extract_skills(extracted_text)
        skills_score = calculate_score(matched_skills)

        keywords_score, matched_keywords, missing_keywords = calculate_keyword_score(
            extracted_text
        )

        experience_score = calculate_experience_score(extracted_text)

        feedback = feedback_generation(
            skills_score,
            keywords_score,
            experience_score,
            missing_skills
        )

        weak_area_result = weak_area(
            skills_score,
            keywords_score,
            experience_score
        )

        missing_keywords_suggestion = keywords_suggestion(missing_keywords)

        final_score = (
            skills_score * 0.40 +
            keywords_score * 0.30 +
            experience_score * 0.30
        )

        final_score = round(final_score, 2)

        resume.skills_score = skills_score
        resume.keywords_score = keywords_score
        resume.experience_score = experience_score
        resume.final_score = final_score
        resume.save()

        nlp = spacy.load("en_core_web_sm")
        doc = nlp(extracted_text)

        NER_words = []

        for ent in doc.ents:
            NER_words.append({
                "text": ent.text,
                "label": ent.label_
            })

        return Response(
            {
                "message": "Resume uploaded successfully.",
                "resume": ResumeSerializer(
                    resume,
                    context={"request": request}
                ).data,
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
                "matched_keywords": matched_keywords,
                "missing_keywords": missing_keywords,
                "NER_words": NER_words,
                "skills_score": skills_score,
                "keywords_score": keywords_score,
                "experience_score": experience_score,
                "final_score": final_score,
                "weak_area": weak_area_result,
                "feedback": feedback,
                "missing_keywords_suggestion": missing_keywords_suggestion,
                "data": data
            },
            status=status.HTTP_201_CREATED
        )

@api_view(["POST"])
@permission_classes([IsAdminUser])
def analyze_resumes(request):
    job_description = request.data.get("job_description", "").strip()

    if not job_description:
        return Response(
            {"error": "Job description is required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    resumes = Resume.objects.all()

    if not resumes.exists():
        return Response(
            {"error": "No resumes available."},
            status=status.HTTP_404_NOT_FOUND
        )

    resume_texts = []
    valid_resumes = []

    for resume in resumes:
        try:
            extracted_text = text_extract(resume.file.path)
            resume_texts.append(extracted_text)
            valid_resumes.append(resume)
        except Exception as error:
            print(f"Error reading {resume.file.name}:", error)

    if not valid_resumes:
        return Response(
            {"error": "Unable to extract resume text."},
            status=status.HTTP_400_BAD_REQUEST
        )

    texts = [job_description] + resume_texts

    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform(texts)

    results = []

    for index, resume in enumerate(valid_resumes):
        job_vector = vectors[0]
        resume_vector = vectors[index + 1]

        similarity = cosine_similarity(
            job_vector,
            resume_vector
        )[0][0]

        similarity_score = round(similarity * 100, 2)

        resume.similarity_score = similarity_score
        resume.save(update_fields=["similarity_score"])

        results.append(
            ResumeSerializer(
                resume,
                context={"request": request}
            ).data
        )

    results.sort(
        key=lambda x: float(x.get("similarity_score", 0)),
        reverse=True
    )

    return Response(
        {
            "message": "Job description analyzed successfully.",
            "job_description": job_description,
            "resumes": results
        },
        status=status.HTTP_200_OK
    )