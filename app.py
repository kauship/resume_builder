from flask import Flask, render_template, request, send_file
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import os

app = Flask(__name__)

# Route for the main page with the form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission and PDF generation
@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    # Retrieve form data
    personal_info = {
        "name": request.form['name'],
        "address": request.form['address'],
        "phone": request.form['phone'],
        "email": request.form['email'],
        "linkedin": request.form['linkedin']
    }
    summary = request.form['summary']
    skills = request.form['skills'].splitlines()
    experience = request.form['experience'].splitlines()
    education = request.form['education']
    certifications = request.form['certifications'].splitlines()
    tech_skills = request.form['tech_skills'].splitlines()
    affiliations = request.form['affiliations'].splitlines()

    # PDF generation
    filename = 'static/resume_preview.pdf'
    doc = SimpleDocTemplate(filename, pagesize=A4, rightMargin=inch, leftMargin=inch, topMargin=inch, bottomMargin=inch)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(name='Title', fontSize=14, leading=14, spaceAfter=10, fontName='Helvetica-Bold')
    section_header = ParagraphStyle(name='SectionHeader', fontSize=12, leading=12, spaceAfter=6, fontName='Helvetica-Bold')
    body_text = styles["BodyText"]

    elements = []

    # Adding content to PDF
    elements.append(Paragraph(f"<b>{personal_info['name']}</b>", title_style))
    elements.append(Paragraph(f"{personal_info['address']}", body_text))
    elements.append(Paragraph(f"{personal_info['phone']} | {personal_info['email']} | {personal_info['linkedin']}", body_text))
    elements.append(Spacer(1, 12))
    
    elements.append(Paragraph("Professional Summary", section_header))
    elements.append(Paragraph(summary, body_text))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Key Skills", section_header))
    skill_text = "<br />".join([f"• {skill}" for skill in skills])
    elements.append(Paragraph(skill_text, body_text))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Professional Experience", section_header))
    experience_text = "<br />".join([f"{exp}" for exp in experience])
    elements.append(Paragraph(experience_text, body_text))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Education", section_header))
    elements.append(Paragraph(education, body_text))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Certifications", section_header))
    cert_text = "<br />".join([f"• {cert}" for cert in certifications])
    elements.append(Paragraph(cert_text, body_text))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Technical Proficiencies", section_header))
    tech_skills_text = "<br />".join([f"• {tech}" for tech in tech_skills])
    elements.append(Paragraph(tech_skills_text, body_text))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Professional Affiliations", section_header))
    affiliations_text = "<br />".join([f"• {affil}" for affil in affiliations])
    elements.append(Paragraph(affiliations_text, body_text))
    
    # Build PDF
    doc.build(elements)

    # Serve the PDF file to the user
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
