from django.db import models

class Resume(models.Model):
    file = models.FileField(upload_to="resumes/")
    skills_score = models.FloatField(default=0)
    keywords_score = models.FloatField(default=0)
    experience_score = models.FloatField(default=0)
    final_score = models.FloatField(default=0)
    similarity_score = models.FloatField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)