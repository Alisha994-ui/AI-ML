from rest_framework import serializers
from .models import Resume

class ResumeSerializer(serializers.ModelSerializer):

    class Meta:

        model = Resume

        fields = [
            "id",
            "file",
            "skills_score",
            "keywords_score",
            "experience_score",
            "similarity_score",
            "final_score",
            "uploaded_at",
        ]