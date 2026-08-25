
def weak_area(skills, keywords, experience):
    scores = {
        "skills_score": skills,
        "keywords_score": keywords,
        "experience_score": experience
    }
    weak_area = min(scores, key=scores.get)
    return weak_area


def keywords_suggestion(missing_keywords):
    suggestions = []
    if missing_keywords:
        suggestions.append(
            "Add relevant keywords such as " +
            ", ".join(missing_keywords) +
            " to your resume where they accurately describe your experience."
        )
    return suggestions


def feedback_generation(skills, keywords, experience, missing_skills):
    suggestions = []
    if missing_skills:
        suggestions.append(
            "Consider adding these missing skills if you have relevant experience: "
            + ", ".join(missing_skills)
            + "."
        )

    if experience < 60:
        suggestions.append(
            "Add more project or work experience details, including your role, responsibilities, and technologies used."
        )

    if skills < 60:
        suggestions.append(
            "Add more relevant technical skills that match your target role and describe where you used them."
        )

    if keywords < 60:
        suggestions.append(
            "Add relevant job-specific keywords from the target role where they accurately describe your experience."
        )

    if not suggestions:
        suggestions.append(
            "Your resume has good coverage of skills, keywords, and experience. Keep the details specific and relevant to the target role."
        )

    return suggestions