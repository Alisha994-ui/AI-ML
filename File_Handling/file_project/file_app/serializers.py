from rest_framework import serializers
from .models import Resume


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = [
            "id",
            "file",
            "uploaded_at",
            "skills_score",
            "keywords_score",
            "experience_score",
            "final_score",
        ]