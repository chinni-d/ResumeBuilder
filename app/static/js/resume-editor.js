// Resume Editor with Live Preview

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('resumeForm');
    const preview = document.getElementById('resumePreview');
    
    // Initialize preview
    updatePreview();
    
    // Add event listeners for real-time updates
    form.addEventListener('input', updatePreview);
    form.addEventListener('change', updatePreview);
    
    // Dynamic form management
    setupDynamicForms();
    
    // Save functionality
    const saveBtn = document.getElementById('saveResume');
    if (saveBtn) {
        // Function to reset button state
        function resetSaveButton() {
            saveBtn.innerHTML = '<i class="fas fa-save me-2"></i>Save Resume';
            saveBtn.disabled = false;
        }
        
        // Reset on page load
        resetSaveButton();
        
        // Reset when page becomes visible (handles back navigation)
        document.addEventListener('visibilitychange', function() {
            if (!document.hidden) {
                resetSaveButton();
            }
        });
        
        // Reset on page focus (additional safety)
        window.addEventListener('focus', resetSaveButton);
        
        saveBtn.addEventListener('click', saveResume);
    }
    
    function updatePreview() {
        const formData = new FormData(form);
        const data = {};
        
        // Collect form data
        for (let [key, value] of formData.entries()) {
            if (key.endsWith('[]')) {
                const arrayKey = key.slice(0, -2);
                if (!data[arrayKey]) data[arrayKey] = [];
                data[arrayKey].push(value);
            } else {
                data[key] = value;
            }
        }
        
        // Generate preview HTML
        const templateId = data.template_id || '1';
        preview.className = `resume-preview template-${templateId}`;
        preview.innerHTML = generatePreviewHTML(data);
    }
    
    function generatePreviewHTML(data) {
        let html = '';
        
        // Header
        html += '<div class="header">';
        const fullName = data.full_name && data.full_name.trim() ? data.full_name : 'Your Name';
        const isNamePlaceholder = !(data.full_name && data.full_name.trim());
        html += `<div class="name ${isNamePlaceholder ? 'placeholder-text' : ''}">${escapeHtml(fullName)}</div>`;
        
        const contactInfo = [];
        const email = data.email && data.email.trim() ? data.email : 'yourname@email.com';
        const phone = data.phone && data.phone.trim() ? data.phone : '+1 (555) 123-4567';
        const address = data.address && data.address.trim() ? data.address : '123 Main St, City, State 12345';
        const linkedin = data.linkedin && data.linkedin.trim() ? data.linkedin : 'https://linkedin.com/in/yourname';
        const github = data.github && data.github.trim() ? data.github : 'https://github.com/yourname';
        
        const isEmailPlaceholder = !(data.email && data.email.trim());
        const isPhonePlaceholder = !(data.phone && data.phone.trim());
        const isAddressPlaceholder = !(data.address && data.address.trim());
        const isLinkedinPlaceholder = !(data.linkedin && data.linkedin.trim());
        const isGithubPlaceholder = !(data.github && data.github.trim());
        
        contactInfo.push(`<span class="${isEmailPlaceholder ? 'placeholder-text' : ''}">${escapeHtml(email)}</span>`);
        contactInfo.push(`<span class="${isPhonePlaceholder ? 'placeholder-text' : ''}">${escapeHtml(phone)}</span>`);
        contactInfo.push(`<span class="${isAddressPlaceholder ? 'placeholder-text' : ''}">${escapeHtml(address)}</span>`);
        contactInfo.push(`<span class="${isLinkedinPlaceholder ? 'placeholder-text' : ''}">${escapeHtml(linkedin)}</span>`);
        contactInfo.push(`<span class="${isGithubPlaceholder ? 'placeholder-text' : ''}">${escapeHtml(github)}</span>`);
        
        html += `<div class="contact">${contactInfo.join(' | ')}</div>`;
        html += '</div>';
        
        // Professional Summary
        if (data.summary && data.summary.trim()) {
            html += '<div class="section">';
            html += '<div class="section-title">Professional Summary</div>';
            html += `<div>${escapeHtml(data.summary).replace(/\n/g, '<br>')}</div>`;
            html += '</div>';
        }
        
        // Skills with ratings
        if (data.skill_name && data.skill_name.some(skill => skill.trim())) {
            html += '<div class="section">';
            html += '<div class="section-title">Skills</div>';
            html += '<div class="skills">';
            
            for (let i = 0; i < data.skill_name.length; i++) {
                if (data.skill_name[i] && data.skill_name[i].trim()) {
                    const level = data.skill_level && data.skill_level[i] ? parseInt(data.skill_level[i]) : 3;
                    const stars = '★'.repeat(level) + '☆'.repeat(5 - level);
                    html += `<div class="skill-item">${escapeHtml(data.skill_name[i])} <span class="skill-rating">${stars}</span></div>`;
                }
            }
            html += '</div></div>';
        }
        
        // Professional Experience
        if (data.experience_title && data.experience_title.some(title => title.trim())) {
            html += '<div class="section">';
            html += '<div class="section-title">Professional Experience</div>';
            
            for (let i = 0; i < data.experience_title.length; i++) {
                if (data.experience_title[i] && data.experience_title[i].trim()) {
                    html += '<div class="experience-item">';
                    html += `<div class="job-title">${escapeHtml(data.experience_title[i])}</div>`;
                    
                    const company = data.experience_company && data.experience_company[i] ? escapeHtml(data.experience_company[i]) : '';
                    const period = data.experience_period && data.experience_period[i] ? escapeHtml(data.experience_period[i]) : '';
                    
                    if (company || period) {
                        html += '<div class="company">';
                        html += company;
                        if (period) {
                            html += `<span class="period">${period}</span>`;
                        }
                        html += '</div>';
                    }
                    
                    if (data.experience_description && data.experience_description[i] && data.experience_description[i].trim()) {
                        html += `<div class="description">${escapeHtml(data.experience_description[i]).replace(/\n/g, '<br>')}</div>`;
                    }
                    
                    html += '</div>';
                }
            }
            html += '</div>';
        }
        
        // Education
        if (data.education_degree && data.education_degree.some(degree => degree.trim())) {
            html += '<div class="section">';
            html += '<div class="section-title">Education</div>';
            
            for (let i = 0; i < data.education_degree.length; i++) {
                if (data.education_degree[i] && data.education_degree[i].trim()) {
                    html += '<div class="education-item">';
                    html += `<div class="job-title">${escapeHtml(data.education_degree[i])}</div>`;
                    
                    const school = data.education_school && data.education_school[i] ? escapeHtml(data.education_school[i]) : '';
                    const year = data.education_year && data.education_year[i] ? escapeHtml(data.education_year[i]) : '';
                    const gpa = data.education_gpa && data.education_gpa[i] ? escapeHtml(data.education_gpa[i]) : '';
                    
                    if (school || year || gpa) {
                        html += '<div class="company">';
                        html += school;
                        if (gpa) html += ` (GPA: ${gpa})`;
                        if (year) {
                            html += `<span class="period">${year}</span>`;
                        }
                        html += '</div>';
                    }
                    
                    html += '</div>';
                }
            }
            html += '</div>';
        }
        
        // Projects
        if (data.project_name && data.project_name.some(name => name.trim())) {
            html += '<div class="section">';
            html += '<div class="section-title">Projects</div>';
            
            for (let i = 0; i < data.project_name.length; i++) {
                if (data.project_name[i] && data.project_name[i].trim()) {
                    html += '<div class="project-item">';
                    html += `<div class="job-title">${escapeHtml(data.project_name[i])}</div>`;
                    
                    if (data.project_description && data.project_description[i] && data.project_description[i].trim()) {
                        html += `<div class="description">${escapeHtml(data.project_description[i]).replace(/\n/g, '<br>')}</div>`;
                    }
                    
                    if (data.project_technologies && data.project_technologies[i] && data.project_technologies[i].trim()) {
                        html += `<div class="description"><strong>Technologies:</strong> ${escapeHtml(data.project_technologies[i])}</div>`;
                    }
                    
                    if (data.project_link && data.project_link[i] && data.project_link[i].trim()) {
                        html += `<div class="description"><strong>Link:</strong> ${escapeHtml(data.project_link[i])}</div>`;
                    }
                    
                    html += '</div>';
                }
            }
            html += '</div>';
        }
        
        // Certifications
        if (data.cert_name && data.cert_name.some(name => name.trim())) {
            html += '<div class="section">';
            html += '<div class="section-title">Certifications</div>';
            
            for (let i = 0; i < data.cert_name.length; i++) {
                if (data.cert_name[i] && data.cert_name[i].trim()) {
                    html += '<div class="cert-item">';
                    html += `<div class="job-title">${escapeHtml(data.cert_name[i])}</div>`;
                    
                    const issuer = data.cert_issuer && data.cert_issuer[i] ? escapeHtml(data.cert_issuer[i]) : '';
                    const date = data.cert_date && data.cert_date[i] ? escapeHtml(data.cert_date[i]) : '';
                    
                    if (issuer || date) {
                        html += '<div class="company">';
                        html += issuer;
                        if (date) {
                            html += `<span class="period">${date}</span>`;
                        }
                        html += '</div>';
                    }
                    
                    html += '</div>';
                }
            }
            html += '</div>';
        }
        
        // Awards
        if (data.award_name && data.award_name.some(name => name.trim())) {
            html += '<div class="section">';
            html += '<div class="section-title">Awards & Achievements</div>';
            
            for (let i = 0; i < data.award_name.length; i++) {
                if (data.award_name[i] && data.award_name[i].trim()) {
                    html += '<div class="award-item">';
                    html += `<div class="job-title">${escapeHtml(data.award_name[i])}</div>`;
                    
                    if (data.award_description && data.award_description[i] && data.award_description[i].trim()) {
                        html += `<div class="description">${escapeHtml(data.award_description[i])}</div>`;
                    }
                    
                    if (data.award_date && data.award_date[i] && data.award_date[i].trim()) {
                        html += `<div class="company"><span class="period">${escapeHtml(data.award_date[i])}</span></div>`;
                    }
                    
                    html += '</div>';
                }
            }
            html += '</div>';
        }
        
        // Languages
        if (data.language_name && data.language_name.some(name => name.trim())) {
            html += '<div class="section">';
            html += '<div class="section-title">Languages</div>';
            html += '<div class="skills">';
            
            for (let i = 0; i < data.language_name.length; i++) {
                if (data.language_name[i] && data.language_name[i].trim()) {
                    const level = data.language_level && data.language_level[i] ? data.language_level[i] : 'Intermediate';
                    html += `<div class="skill-item">${escapeHtml(data.language_name[i])} (${level})</div>`;
                }
            }
            html += '</div></div>';
        }
        
        // Hobbies
        if (data.hobbies && data.hobbies.some(hobby => hobby.trim())) {
            const validHobbies = data.hobbies.filter(hobby => hobby.trim());
            html += '<div class="section">';
            html += '<div class="section-title">Hobbies & Interests</div>';
            html += `<div class="skills">${validHobbies.map(escapeHtml).join(', ')}</div>`;
            html += '</div>';
        }
        
        return html || '<div class="text-muted text-center py-5">Start filling out the form to see your resume preview</div>';
    }
    
    function setupDynamicForms() {
        // Skills management
        document.getElementById('addSkill').addEventListener('click', function() {
            const container = document.getElementById('skillsContainer');
            const skillItem = document.createElement('div');
            skillItem.className = 'row mb-2 skill-item';
            skillItem.innerHTML = `
                <div class="col-8">
                    <input type="text" class="form-control" name="skill_name[]" placeholder="Skill name">
                </div>
                <div class="col-3">
                    <select class="form-select" name="skill_level[]">
                        <option value="1">⭐</option>
                        <option value="2">⭐⭐</option>
                        <option value="3" selected>⭐⭐⭐</option>
                        <option value="4">⭐⭐⭐⭐</option>
                        <option value="5">⭐⭐⭐⭐⭐</option>
                    </select>
                </div>
                <div class="col-1">
                    <button type="button" class="btn btn-outline-danger btn-sm remove-skill">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            `;
            container.appendChild(skillItem);
            
            skillItem.querySelector('.remove-skill').addEventListener('click', function() {
                skillItem.remove();
                updatePreview();
            });
            
            skillItem.querySelectorAll('input, select').forEach(input => {
                input.addEventListener('input', updatePreview);
                input.addEventListener('change', updatePreview);
            });
        });
        
        // Experience management
        document.getElementById('addExperience').addEventListener('click', function() {
            const container = document.getElementById('experienceContainer');
            const expItem = document.createElement('div');
            expItem.className = 'experience-item border p-3 mb-3 rounded';
            expItem.innerHTML = `
                <div class="row">
                    <div class="col-md-6 mb-2">
                        <input type="text" class="form-control" name="experience_title[]" placeholder="Job Title">
                    </div>
                    <div class="col-md-6 mb-2">
                        <input type="text" class="form-control" name="experience_company[]" placeholder="Company">
                    </div>
                </div>
                <div class="mb-2">
                    <input type="text" class="form-control" name="experience_period[]" placeholder="e.g., Jan 2020 - Present">
                </div>
                <div class="mb-2">
                    <textarea class="form-control" name="experience_description[]" rows="3" placeholder="Job description and achievements..."></textarea>
                </div>
                <button type="button" class="btn btn-outline-danger btn-sm remove-experience">
                    <i class="fas fa-trash me-1"></i>Remove
                </button>
            `;
            container.appendChild(expItem);
            
            expItem.querySelector('.remove-experience').addEventListener('click', function() {
                expItem.remove();
                updatePreview();
            });
            
            expItem.querySelectorAll('input, textarea').forEach(input => {
                input.addEventListener('input', updatePreview);
            });
        });
        
        // Education management
        document.getElementById('addEducation').addEventListener('click', function() {
            const container = document.getElementById('educationContainer');
            const eduItem = document.createElement('div');
            eduItem.className = 'education-item border p-3 mb-3 rounded';
            eduItem.innerHTML = `
                <div class="row">
                    <div class="col-md-6 mb-2">
                        <input type="text" class="form-control" name="education_degree[]" placeholder="Degree">
                    </div>
                    <div class="col-md-6 mb-2">
                        <input type="text" class="form-control" name="education_school[]" placeholder="School/University">
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-6 mb-2">
                        <input type="text" class="form-control" name="education_year[]" placeholder="Year">
                    </div>
                    <div class="col-md-6 mb-2">
                        <input type="text" class="form-control" name="education_gpa[]" placeholder="GPA (optional)">
                    </div>
                </div>
                <button type="button" class="btn btn-outline-danger btn-sm remove-education">
                    <i class="fas fa-trash me-1"></i>Remove
                </button>
            `;
            container.appendChild(eduItem);
            
            eduItem.querySelector('.remove-education').addEventListener('click', function() {
                eduItem.remove();
                updatePreview();
            });
            
            eduItem.querySelectorAll('input').forEach(input => {
                input.addEventListener('input', updatePreview);
            });
        });
        
        // Projects management
        document.getElementById('addProject').addEventListener('click', function() {
            const container = document.getElementById('projectsContainer');
            const projItem = document.createElement('div');
            projItem.className = 'project-item border p-3 mb-3 rounded';
            projItem.innerHTML = `
                <div class="mb-2">
                    <input type="text" class="form-control" name="project_name[]" placeholder="Project Name">
                </div>
                <div class="mb-2">
                    <textarea class="form-control" name="project_description[]" rows="2" placeholder="Project description..."></textarea>
                </div>
                <div class="row">
                    <div class="col-md-6 mb-2">
                        <input type="text" class="form-control" name="project_technologies[]" placeholder="Technologies used">
                    </div>
                    <div class="col-md-6 mb-2">
                        <input type="url" class="form-control" name="project_link[]" placeholder="Project link (optional)">
                    </div>
                </div>
                <button type="button" class="btn btn-outline-danger btn-sm remove-project">
                    <i class="fas fa-trash me-1"></i>Remove
                </button>
            `;
            container.appendChild(projItem);
            
            projItem.querySelector('.remove-project').addEventListener('click', function() {
                projItem.remove();
                updatePreview();
            });
            
            projItem.querySelectorAll('input, textarea').forEach(input => {
                input.addEventListener('input', updatePreview);
            });
        });
        
        // Certifications management
        document.getElementById('addCert').addEventListener('click', function() {
            const container = document.getElementById('certificationsContainer');
            const certItem = document.createElement('div');
            certItem.className = 'cert-item border p-3 mb-3 rounded';
            certItem.innerHTML = `
                <div class="row">
                    <div class="col-md-6 mb-2">
                        <input type="text" class="form-control" name="cert_name[]" placeholder="Certification Name">
                    </div>
                    <div class="col-md-6 mb-2">
                        <input type="text" class="form-control" name="cert_issuer[]" placeholder="Issuing Organization">
                    </div>
                </div>
                <div class="mb-2">
                    <input type="text" class="form-control" name="cert_date[]" placeholder="Date obtained">
                </div>
                <button type="button" class="btn btn-outline-danger btn-sm remove-cert">
                    <i class="fas fa-trash me-1"></i>Remove
                </button>
            `;
            container.appendChild(certItem);
            
            certItem.querySelector('.remove-cert').addEventListener('click', function() {
                certItem.remove();
                updatePreview();
            });
            
            certItem.querySelectorAll('input').forEach(input => {
                input.addEventListener('input', updatePreview);
            });
        });
        
        // Awards management
        document.getElementById('addAward').addEventListener('click', function() {
            const container = document.getElementById('awardsContainer');
            const awardItem = document.createElement('div');
            awardItem.className = 'award-item border p-3 mb-3 rounded';
            awardItem.innerHTML = `
                <div class="row">
                    <div class="col-md-6 mb-2">
                        <input type="text" class="form-control" name="award_name[]" placeholder="Award Name">
                    </div>
                    <div class="col-md-6 mb-2">
                        <input type="text" class="form-control" name="award_date[]" placeholder="Date received">
                    </div>
                </div>
                <div class="mb-2">
                    <textarea class="form-control" name="award_description[]" rows="2" placeholder="Award description..."></textarea>
                </div>
                <button type="button" class="btn btn-outline-danger btn-sm remove-award">
                    <i class="fas fa-trash me-1"></i>Remove
                </button>
            `;
            container.appendChild(awardItem);
            
            awardItem.querySelector('.remove-award').addEventListener('click', function() {
                awardItem.remove();
                updatePreview();
            });
            
            awardItem.querySelectorAll('input, textarea').forEach(input => {
                input.addEventListener('input', updatePreview);
            });
        });
        
        // Languages management
        document.getElementById('addLanguage').addEventListener('click', function() {
            const container = document.getElementById('languagesContainer');
            const langItem = document.createElement('div');
            langItem.className = 'row mb-2 language-item';
            langItem.innerHTML = `
                <div class="col-6">
                    <input type="text" class="form-control" name="language_name[]" placeholder="Language">
                </div>
                <div class="col-5">
                    <select class="form-select" name="language_level[]">
                        <option value="Beginner">Beginner</option>
                        <option value="Intermediate" selected>Intermediate</option>
                        <option value="Advanced">Advanced</option>
                        <option value="Fluent">Fluent</option>
                        <option value="Native">Native</option>
                    </select>
                </div>
                <div class="col-1">
                    <button type="button" class="btn btn-outline-danger btn-sm remove-language">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            `;
            container.appendChild(langItem);
            
            langItem.querySelector('.remove-language').addEventListener('click', function() {
                langItem.remove();
                updatePreview();
            });
            
            langItem.querySelectorAll('input, select').forEach(input => {
                input.addEventListener('input', updatePreview);
                input.addEventListener('change', updatePreview);
            });
        });
        
        // Hobbies management
        document.getElementById('addHobby').addEventListener('click', function() {
            const container = document.getElementById('hobbiesContainer');
            const hobbyItem = document.createElement('div');
            hobbyItem.className = 'input-group mb-2 hobby-item';
            hobbyItem.innerHTML = `
                <input type="text" class="form-control" name="hobbies[]" placeholder="Enter a hobby">
                <button type="button" class="btn btn-outline-danger remove-hobby">
                    <i class="fas fa-times"></i>
                </button>
            `;
            container.appendChild(hobbyItem);
            
            hobbyItem.querySelector('.remove-hobby').addEventListener('click', function() {
                hobbyItem.remove();
                updatePreview();
            });
            
            hobbyItem.querySelector('input').addEventListener('input', updatePreview);
        });
        
        // Add event listeners to existing remove buttons
        document.querySelectorAll('.remove-skill').forEach(btn => {
            btn.addEventListener('click', function() {
                btn.closest('.skill-item').remove();
                updatePreview();
            });
        });
        
        document.querySelectorAll('.remove-experience').forEach(btn => {
            btn.addEventListener('click', function() {
                btn.closest('.experience-item').remove();
                updatePreview();
            });
        });
        
        document.querySelectorAll('.remove-education').forEach(btn => {
            btn.addEventListener('click', function() {
                btn.closest('.education-item').remove();
                updatePreview();
            });
        });
        
        document.querySelectorAll('.remove-project').forEach(btn => {
            btn.addEventListener('click', function() {
                btn.closest('.project-item').remove();
                updatePreview();
            });
        });
        
        document.querySelectorAll('.remove-cert').forEach(btn => {
            btn.addEventListener('click', function() {
                btn.closest('.cert-item').remove();
                updatePreview();
            });
        });
        
        document.querySelectorAll('.remove-award').forEach(btn => {
            btn.addEventListener('click', function() {
                btn.closest('.award-item').remove();
                updatePreview();
            });
        });
        
        document.querySelectorAll('.remove-language').forEach(btn => {
            btn.addEventListener('click', function() {
                btn.closest('.language-item').remove();
                updatePreview();
            });
        });
        
        document.querySelectorAll('.remove-hobby').forEach(btn => {
            btn.addEventListener('click', function() {
                btn.closest('.hobby-item').remove();
                updatePreview();
            });
        });
    }
    
    function saveResume() {
        const saveBtn = document.getElementById('saveResume');
        const originalText = saveBtn.innerHTML;
        
        saveBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Saving...';
        saveBtn.disabled = true;
        
        const form = document.getElementById('resumeForm');
        const resumeId = document.getElementById('resumeId').value;
        
        // Submit form normally to redirect to save page
        form.action = `/save/${resumeId}`;
        form.method = 'POST';
        form.submit();
    }
    
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
});