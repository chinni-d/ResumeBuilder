import re
from collections import Counter

def calculate_ats_score(resume_content):
    """Calculate ATS score based on resume content"""
    score = 0
    max_score = 100
    
    if not resume_content:
        return 0
    
    # Basic Information (20 points)
    if resume_content.full_name:
        score += 5
    if resume_content.email and '@' in resume_content.email:
        score += 5
    if resume_content.phone:
        score += 5
    if resume_content.address:
        score += 5
    
    # Professional Summary (15 points)
    if resume_content.summary:
        summary_words = len(resume_content.summary.split())
        if summary_words >= 50:
            score += 15
        elif summary_words >= 25:
            score += 10
        elif summary_words >= 10:
            score += 5
    
    # Skills Section (20 points)
    skills = resume_content.get_skills()
    if skills:
        skill_count = len(skills)
        if skill_count >= 10:
            score += 20
        elif skill_count >= 6:
            score += 15
        elif skill_count >= 3:
            score += 10
        else:
            score += 5
    
    # Experience Section (25 points)
    experience = resume_content.get_experience()
    if experience:
        exp_count = len(experience)
        total_desc_words = 0
        
        for exp in experience:
            if exp.get('description'):
                total_desc_words += len(exp['description'].split())
        
        if exp_count >= 3 and total_desc_words >= 150:
            score += 25
        elif exp_count >= 2 and total_desc_words >= 100:
            score += 20
        elif exp_count >= 1 and total_desc_words >= 50:
            score += 15
        else:
            score += 10
    
    # Education Section (10 points)
    education = resume_content.get_education()
    if education and len(education) > 0:
        score += 10
    
    # Additional Sections (10 points)
    additional_sections = 0
    if resume_content.get_projects():
        additional_sections += 1
    if resume_content.get_certifications():
        additional_sections += 1
    if resume_content.get_awards():
        additional_sections += 1
    if resume_content.get_languages():
        additional_sections += 1
    
    if additional_sections >= 3:
        score += 10
    elif additional_sections >= 2:
        score += 7
    elif additional_sections >= 1:
        score += 5
    
    return min(score, max_score)

def get_ats_recommendations(resume_content):
    """Get ATS improvement recommendations"""
    recommendations = []
    
    if not resume_content:
        return ["Please add content to your resume"]
    
    # Check basic info
    if not resume_content.full_name:
        recommendations.append("Add your full name")
    if not resume_content.email:
        recommendations.append("Add your email address")
    if not resume_content.phone:
        recommendations.append("Add your phone number")
    
    # Check summary
    if not resume_content.summary:
        recommendations.append("Add a professional summary")
    elif len(resume_content.summary.split()) < 25:
        recommendations.append("Expand your professional summary (aim for 25-50 words)")
    
    # Check skills
    skills = resume_content.get_skills()
    if not skills:
        recommendations.append("Add relevant skills to your resume")
    elif len(skills) < 6:
        recommendations.append("Add more skills (aim for 6-10 relevant skills)")
    
    # Check experience
    experience = resume_content.get_experience()
    if not experience:
        recommendations.append("Add work experience")
    else:
        for i, exp in enumerate(experience):
            if not exp.get('description') or len(exp['description'].split()) < 20:
                recommendations.append(f"Add more detailed description for experience #{i+1}")
    
    # Check education
    if not resume_content.get_education():
        recommendations.append("Add your education background")
    
    # Suggest additional sections
    if not resume_content.get_projects():
        recommendations.append("Consider adding relevant projects")
    if not resume_content.get_certifications():
        recommendations.append("Add any relevant certifications")
    
    return recommendations[:5]  # Return top 5 recommendations