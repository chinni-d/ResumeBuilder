from datetime import datetime
from app import db
import json

class Resume(db.Model):
    __tablename__ = 'resumes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    template_id = db.Column(db.Integer, default=1)
    ats_score = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with resume content
    content = db.relationship('ResumeContent', backref='resume', uselist=False, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Resume {self.title}>'

class ResumeContent(db.Model):
    __tablename__ = 'resume_content'
    
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=False)
    
    # Personal Information
    full_name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    linkedin = db.Column(db.String(200))
    github = db.Column(db.String(200))
    website = db.Column(db.String(200))
    
    # Professional Summary
    summary = db.Column(db.Text)
    
    # Skills with ratings (stored as JSON)
    skills = db.Column(db.Text)  # JSON: [{"name": "Python", "level": 5}, ...]
    
    # Education (stored as JSON)
    education = db.Column(db.Text)  # JSON string
    
    # Experience (stored as JSON)
    experience = db.Column(db.Text)  # JSON string
    
    # Projects (stored as JSON)
    projects = db.Column(db.Text)  # JSON string
    
    # New sections
    certifications = db.Column(db.Text)  # JSON string
    awards = db.Column(db.Text)  # JSON string
    languages = db.Column(db.Text)  # JSON: [{"name": "English", "level": "Native"}, ...]
    hobbies = db.Column(db.Text)  # JSON array of strings
    
    def get_skills(self):
        """Get skills as list with ratings"""
        return json.loads(self.skills) if self.skills else []
    
    def set_skills(self, skills_list):
        """Set skills from list"""
        self.skills = json.dumps(skills_list)
    
    def get_education(self):
        """Get education as list"""
        return json.loads(self.education) if self.education else []
    
    def set_education(self, education_list):
        """Set education from list"""
        self.education = json.dumps(education_list)
    
    def get_experience(self):
        """Get experience as list"""
        return json.loads(self.experience) if self.experience else []
    
    def set_experience(self, experience_list):
        """Set experience from list"""
        self.experience = json.dumps(experience_list)
    
    def get_projects(self):
        """Get projects as list"""
        return json.loads(self.projects) if self.projects else []
    
    def set_projects(self, projects_list):
        """Set projects from list"""
        self.projects = json.dumps(projects_list)
    
    def get_certifications(self):
        """Get certifications as list"""
        return json.loads(self.certifications) if self.certifications else []
    
    def set_certifications(self, cert_list):
        """Set certifications from list"""
        self.certifications = json.dumps(cert_list)
    
    def get_awards(self):
        """Get awards as list"""
        return json.loads(self.awards) if self.awards else []
    
    def set_awards(self, awards_list):
        """Set awards from list"""
        self.awards = json.dumps(awards_list)
    
    def get_languages(self):
        """Get languages as list"""
        return json.loads(self.languages) if self.languages else []
    
    def set_languages(self, lang_list):
        """Set languages from list"""
        self.languages = json.dumps(lang_list)
    
    def get_hobbies(self):
        """Get hobbies as list"""
        return json.loads(self.hobbies) if self.hobbies else []
    
    def set_hobbies(self, hobbies_list):
        """Set hobbies from list"""
        self.hobbies = json.dumps(hobbies_list)