from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response
from flask_login import login_required, current_user
from app.models.resume import Resume, ResumeContent
from app.utils.export import export_to_docx
from app.utils.ats_scorer import calculate_ats_score, get_ats_recommendations
from app import db

resume_bp = Blueprint('resume', __name__)

@resume_bp.route('/create')
@login_required
def create():
    return render_template('resume/create.html')

@resume_bp.route('/create', methods=['POST'])
@login_required
def create_post():
    title = request.form.get('title', 'My Resume')
    template_id = int(request.form.get('template_id', 1))
    
    # Create new resume
    resume = Resume(user_id=current_user.id, title=title, template_id=template_id)
    db.session.add(resume)
    db.session.flush()  # Get the resume ID
    
    # Create empty content
    content = ResumeContent(resume_id=resume.id)
    db.session.add(content)
    
    try:
        db.session.commit()
        flash('Resume created successfully!', 'success')
        return redirect(url_for('resume.edit', id=resume.id))
    except Exception as e:
        db.session.rollback()
        flash('Failed to create resume.', 'error')
        return redirect(url_for('main.dashboard'))

@resume_bp.route('/edit/<int:id>')
@login_required
def edit(id):
    resume = Resume.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    if not resume.content:
        content = ResumeContent(resume_id=resume.id)
        db.session.add(content)
        db.session.commit()
    return render_template('resume/edit.html', resume=resume)

@resume_bp.route('/save/<int:id>', methods=['POST'])
@login_required
def save(id):
    resume = Resume.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    if not resume.content:
        content = ResumeContent(resume_id=resume.id)
        db.session.add(content)
        db.session.flush()
    else:
        content = resume.content
    
    # Update content from form data
    content.full_name = request.form.get('full_name', '')
    content.email = request.form.get('email', '')
    content.phone = request.form.get('phone', '')
    content.address = request.form.get('address', '')
    content.linkedin = request.form.get('linkedin', '')
    content.github = request.form.get('github', '')
    content.summary = request.form.get('summary', '')
    
    # Handle Skills with ratings
    skills_data = []
    skill_names = request.form.getlist('skill_name[]')
    skill_levels = request.form.getlist('skill_level[]')
    
    for i in range(len(skill_names)):
        if skill_names[i].strip():
            skills_data.append({
                'name': skill_names[i],
                'level': int(skill_levels[i]) if i < len(skill_levels) and skill_levels[i] else 3
            })
    content.set_skills(skills_data)
    
    # Education
    education_data = []
    edu_degrees = request.form.getlist('education_degree[]')
    edu_schools = request.form.getlist('education_school[]')
    edu_years = request.form.getlist('education_year[]')
    edu_gpas = request.form.getlist('education_gpa[]')
    
    for i in range(len(edu_degrees)):
        if edu_degrees[i].strip():
            education_data.append({
                'degree': edu_degrees[i],
                'school': edu_schools[i] if i < len(edu_schools) else '',
                'year': edu_years[i] if i < len(edu_years) else '',
                'gpa': edu_gpas[i] if i < len(edu_gpas) else ''
            })
    content.set_education(education_data)
    
    # Experience
    experience_data = []
    exp_titles = request.form.getlist('experience_title[]')
    exp_companies = request.form.getlist('experience_company[]')
    exp_periods = request.form.getlist('experience_period[]')
    exp_descriptions = request.form.getlist('experience_description[]')
    
    for i in range(len(exp_titles)):
        if exp_titles[i].strip():
            experience_data.append({
                'title': exp_titles[i],
                'company': exp_companies[i] if i < len(exp_companies) else '',
                'period': exp_periods[i] if i < len(exp_periods) else '',
                'description': exp_descriptions[i] if i < len(exp_descriptions) else ''
            })
    content.set_experience(experience_data)
    
    # Projects
    projects_data = []
    proj_names = request.form.getlist('project_name[]')
    proj_descriptions = request.form.getlist('project_description[]')
    proj_technologies = request.form.getlist('project_technologies[]')
    proj_links = request.form.getlist('project_link[]')
    
    for i in range(len(proj_names)):
        if proj_names[i].strip():
            projects_data.append({
                'name': proj_names[i],
                'description': proj_descriptions[i] if i < len(proj_descriptions) else '',
                'technologies': proj_technologies[i] if i < len(proj_technologies) else '',
                'link': proj_links[i] if i < len(proj_links) else ''
            })
    content.set_projects(projects_data)
    
    # Certifications
    cert_data = []
    cert_names = request.form.getlist('cert_name[]')
    cert_issuers = request.form.getlist('cert_issuer[]')
    cert_dates = request.form.getlist('cert_date[]')
    
    for i in range(len(cert_names)):
        if cert_names[i].strip():
            cert_data.append({
                'name': cert_names[i],
                'issuer': cert_issuers[i] if i < len(cert_issuers) else '',
                'date': cert_dates[i] if i < len(cert_dates) else ''
            })
    content.set_certifications(cert_data)
    
    # Awards
    award_data = []
    award_names = request.form.getlist('award_name[]')
    award_descriptions = request.form.getlist('award_description[]')
    award_dates = request.form.getlist('award_date[]')
    
    for i in range(len(award_names)):
        if award_names[i].strip():
            award_data.append({
                'name': award_names[i],
                'description': award_descriptions[i] if i < len(award_descriptions) else '',
                'date': award_dates[i] if i < len(award_dates) else ''
            })
    content.set_awards(award_data)
    
    # Languages
    lang_data = []
    lang_names = request.form.getlist('language_name[]')
    lang_levels = request.form.getlist('language_level[]')
    
    for i in range(len(lang_names)):
        if lang_names[i].strip():
            lang_data.append({
                'name': lang_names[i],
                'level': lang_levels[i] if i < len(lang_levels) else 'Intermediate'
            })
    content.set_languages(lang_data)
    
    # Hobbies
    hobbies = request.form.getlist('hobbies[]')
    content.set_hobbies([hobby for hobby in hobbies if hobby.strip()])
    
    # Update resume title and template
    resume.title = request.form.get('resume_title', resume.title)
    resume.template_id = int(request.form.get('template_id', resume.template_id))
    
    # Calculate ATS score
    resume.ats_score = calculate_ats_score(content)
    
    try:
        db.session.commit()
        return redirect(url_for('resume.save_page', id=resume.id))
    except Exception as e:
        db.session.rollback()
        flash('Failed to save resume.', 'error')
        return redirect(url_for('resume.edit', id=resume.id))

@resume_bp.route('/save-page/<int:id>')
@login_required
def save_page(id):
    resume = Resume.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    recommendations = get_ats_recommendations(resume.content) if resume.content else []
    preview_html = generate_preview_html(resume.content) if resume.content else ''
    return render_template('resume/save.html', resume=resume, recommendations=recommendations, preview_html=preview_html)

def generate_preview_html(content):
    if not content:
        return '<div class="text-muted text-center py-5">No content available</div>'
    
    html = ''
    
    # Header
    html += '<div class="header">'
    if content.full_name:
        html += f'<div class="name">{content.full_name}</div>'
    
    contact_info = []
    if content.email: contact_info.append(content.email)
    if content.phone: contact_info.append(content.phone)
    if content.address: contact_info.append(content.address)
    if content.linkedin: contact_info.append(content.linkedin)
    if content.github: contact_info.append(content.github)
    
    if contact_info:
        html += f'<div class="contact">{" | ".join(contact_info)}</div>'
    html += '</div>'
    
    # Professional Summary
    if content.summary and content.summary.strip():
        html += '<div class="section">'
        html += '<div class="section-title">Professional Summary</div>'
        html += f'<div>{content.summary.replace(chr(10), "<br>")}</div>'
        html += '</div>'
    
    # Skills
    skills = content.get_skills()
    if skills:
        html += '<div class="section">'
        html += '<div class="section-title">Skills</div>'
        html += '<div class="skills">'
        for skill in skills:
            stars = '★' * skill.get('level', 3) + '☆' * (5 - skill.get('level', 3))
            html += f'<div class="skill-item">{skill.get("name", "")} <span class="skill-rating">{stars}</span></div>'
        html += '</div></div>'
    
    # Experience
    experience = content.get_experience()
    if experience:
        html += '<div class="section">'
        html += '<div class="section-title">Professional Experience</div>'
        for exp in experience:
            html += '<div class="experience-item">'
            html += f'<div class="job-title">{exp.get("title", "")}</div>'
            if exp.get('company') or exp.get('period'):
                html += '<div class="company">'
                html += exp.get('company', '')
                if exp.get('period'):
                    html += f'<span class="period">{exp.get("period", "")}</span>'
                html += '</div>'
            if exp.get('description'):
                html += f'<div class="description">{exp.get("description", "").replace(chr(10), "<br>")}</div>'
            html += '</div>'
        html += '</div>'
    
    # Education
    education = content.get_education()
    if education:
        html += '<div class="section">'
        html += '<div class="section-title">Education</div>'
        for edu in education:
            html += '<div class="education-item">'
            html += f'<div class="job-title">{edu.get("degree", "")}</div>'
            if edu.get('school') or edu.get('year') or edu.get('gpa'):
                html += '<div class="company">'
                html += edu.get('school', '')
                if edu.get('gpa'):
                    html += f' (GPA: {edu.get("gpa", "")})'
                if edu.get('year'):
                    html += f'<span class="period">{edu.get("year", "")}</span>'
                html += '</div>'
            html += '</div>'
        html += '</div>'
    
    # Projects
    projects = content.get_projects()
    if projects:
        html += '<div class="section">'
        html += '<div class="section-title">Projects</div>'
        for proj in projects:
            html += '<div class="project-item">'
            html += f'<div class="job-title">{proj.get("name", "")}</div>'
            if proj.get('description'):
                html += f'<div class="description">{proj.get("description", "").replace(chr(10), "<br>")}</div>'
            if proj.get('technologies'):
                html += f'<div class="description"><strong>Technologies:</strong> {proj.get("technologies", "")}</div>'
            if proj.get('link'):
                html += f'<div class="description"><strong>Link:</strong> {proj.get("link", "")}</div>'
            html += '</div>'
        html += '</div>'
    
    # Certifications
    certifications = content.get_certifications()
    if certifications:
        html += '<div class="section">'
        html += '<div class="section-title">Certifications</div>'
        for cert in certifications:
            html += '<div class="cert-item">'
            html += f'<div class="job-title">{cert.get("name", "")}</div>'
            if cert.get('issuer') or cert.get('date'):
                html += '<div class="company">'
                html += cert.get('issuer', '')
                if cert.get('date'):
                    html += f'<span class="period">{cert.get("date", "")}</span>'
                html += '</div>'
            html += '</div>'
        html += '</div>'
    
    # Awards
    awards = content.get_awards()
    if awards:
        html += '<div class="section">'
        html += '<div class="section-title">Awards & Achievements</div>'
        for award in awards:
            html += '<div class="award-item">'
            html += f'<div class="job-title">{award.get("name", "")}</div>'
            if award.get('description'):
                html += f'<div class="description">{award.get("description", "")}</div>'
            if award.get('date'):
                html += f'<div class="company"><span class="period">{award.get("date", "")}</span></div>'
            html += '</div>'
        html += '</div>'
    
    # Languages
    languages = content.get_languages()
    if languages:
        html += '<div class="section">'
        html += '<div class="section-title">Languages</div>'
        html += '<div class="skills">'
        for lang in languages:
            html += f'<div class="skill-item">{lang.get("name", "")} ({lang.get("level", "Intermediate")})</div>'
        html += '</div></div>'
    
    # Hobbies
    hobbies = content.get_hobbies()
    if hobbies:
        html += '<div class="section">'
        html += '<div class="section-title">Hobbies & Interests</div>'
        html += f'<div class="skills">{", ".join(hobbies)}</div>'
        html += '</div>'
    
    return html or '<div class="text-muted text-center py-5">No content available</div>'
@resume_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    resume = Resume.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    try:
        db.session.delete(resume)
        db.session.commit()
        flash('Resume deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Failed to delete resume.', 'error')
    
    return redirect(url_for('main.dashboard'))

@resume_bp.route('/export/<int:id>/<format>')
@login_required
def export(id, format):
    resume = Resume.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    if format == 'docx':
        return export_to_docx(resume)
    else:
        flash('Invalid export format.', 'error')
        return redirect(url_for('main.dashboard'))