import re
from collections import Counter
import random

class BasicAIAnalyzer:
    def __init__(self):
        self.power_words = [
            'achieved', 'managed', 'led', 'developed', 'created', 'improved', 
            'increased', 'reduced', 'optimized', 'implemented', 'designed',
            'collaborated', 'coordinated', 'supervised', 'executed', 'delivered'
        ]
        
        self.technical_keywords = [
            'python', 'java', 'javascript', 'react', 'node', 'sql', 'aws',
            'docker', 'kubernetes', 'git', 'agile', 'scrum', 'api', 'database',
            'machine learning', 'ai', 'data analysis', 'cloud', 'devops'
        ]
        
        self.soft_skills = [
            'leadership', 'communication', 'teamwork', 'problem solving',
            'analytical', 'creative', 'adaptable', 'organized', 'detail-oriented'
        ]
    
    def analyze_text_quality(self, text):
        if not text:
            return 0
        
        words = text.lower().split()
        score = 0
        
        # Check for power words
        power_word_count = sum(1 for word in words if any(pw in word for pw in self.power_words))
        score += min(power_word_count * 10, 30)
        
        # Check text length and structure
        if len(words) > 20:
            score += 20
        elif len(words) > 10:
            score += 10
        
        # Check for numbers (quantified achievements)
        number_count = len(re.findall(r'\d+', text))
        score += min(number_count * 5, 15)
        
        return min(score, 65)
    
    def analyze_keywords(self, content):
        # Handle skills data structure safely
        skills_text = ''
        skills = content.get('skills', [])
        if skills:
            if isinstance(skills[0], dict):
                skills_text = ' '.join([skill.get('name', '') for skill in skills])
            else:
                skills_text = ' '.join([str(skill) for skill in skills])
        
        all_text = ' '.join([
            content.get('summary', ''),
            skills_text,
            ' '.join([exp.get('description', '') for exp in content.get('experience', [])])
        ]).lower()
        
        tech_matches = sum(1 for keyword in self.technical_keywords if keyword in all_text)
        soft_matches = sum(1 for skill in self.soft_skills if skill in all_text)
        
        return min((tech_matches * 3) + (soft_matches * 2), 35)

def calculate_ats_score(resume_content):
    """AI-based ATS score calculation"""
    if not resume_content:
        return 0
    
    analyzer = BasicAIAnalyzer()
    
    # Convert resume_content to dict format for analysis
    skills_data = resume_content.get_skills() or []
    # Handle both dict and string formats for skills
    if skills_data and isinstance(skills_data[0], dict):
        skills_list = skills_data
    else:
        skills_list = [{'name': str(skill)} for skill in skills_data]
    
    content_dict = {
        'summary': getattr(resume_content, 'summary', ''),
        'skills': skills_list,
        'experience': resume_content.get_experience() or [],
        'education': resume_content.get_education() or [],
        'projects': resume_content.get_projects() or [],
        'certifications': resume_content.get_certifications() or []
    }
    
    # AI-based scoring components
    completeness_score = _assess_completeness(resume_content)
    quality_score = analyzer.analyze_text_quality(content_dict['summary'])
    keyword_score = analyzer.analyze_keywords(content_dict)
    
    # Weighted final score
    final_score = (completeness_score * 0.4) + (quality_score * 0.35) + (keyword_score * 0.25)
    
    return min(int(final_score), 100)

def _assess_completeness(resume_content):
    """Assess resume completeness using AI logic"""
    score = 0
    
    # Essential fields
    if getattr(resume_content, 'full_name', None):
        score += 15
    if getattr(resume_content, 'email', None):
        score += 15
    if getattr(resume_content, 'phone', None):
        score += 10
    
    # Content sections
    if getattr(resume_content, 'summary', None):
        score += 20
    if resume_content.get_skills():
        score += 15
    if resume_content.get_experience():
        score += 20
    if resume_content.get_education():
        score += 5
    
    return score

def get_ats_recommendations(resume_content):
    """AI-generated recommendations"""
    if not resume_content:
        return ["Please add content to your resume"]
    
    analyzer = BasicAIAnalyzer()
    recommendations = []
    
    # AI-driven analysis
    summary = getattr(resume_content, 'summary', '')
    if not summary:
        recommendations.append("Add a compelling professional summary with quantified achievements")
    elif len(summary.split()) < 30:
        recommendations.append("Expand your summary with more impact-driven content and metrics")
    
    # Skills analysis
    skills = resume_content.get_skills() or []
    if len(skills) < 8:
        recommendations.append("Include more relevant technical and soft skills to match job requirements")
    
    # Experience analysis
    experience = resume_content.get_experience() or []
    if not experience:
        recommendations.append("Add detailed work experience with quantified accomplishments")
    else:
        weak_descriptions = [exp for exp in experience if len(exp.get('description', '').split()) < 25]
        if weak_descriptions:
            recommendations.append("Strengthen job descriptions with action verbs and measurable results")
    
    # Content quality analysis
    all_text = ' '.join([summary] + [exp.get('description', '') for exp in experience])
    power_word_count = sum(1 for word in analyzer.power_words if word in all_text.lower())
    if power_word_count < 3:
        recommendations.append("Use more action verbs like 'achieved', 'led', 'improved' to show impact")
    
    # Additional sections
    if not resume_content.get_projects():
        recommendations.append("Add relevant projects to demonstrate practical skills and experience")
    
    return recommendations[:5]