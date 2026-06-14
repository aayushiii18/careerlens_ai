# CareerLens AI 🚀

### AI-Powered Resume, Portfolio & Skill Gap Analyzer for Students

CareerLens AI is an intelligent career assistance platform designed to help students improve their employability and internship readiness. It generates professional resumes, cover letters, and portfolio content while analyzing skill gaps against target job roles.

The platform helps students identify missing skills, improve career documents, and better align themselves with industry requirements.

---

## Problem Statement

Many students struggle to present their skills, certifications, and projects in a professional and attractive format. Generic resume templates often fail to highlight individual strengths. This reduces internship and placement opportunities.

CareerLens AI addresses this problem by providing an AI-powered solution that automatically generates career documents and analyzes skill readiness.

---

## Features

### Resume Generator

* Generates structured professional resume content
* Highlights skills, projects, education, and certifications

### Cover Letter Generator

* Creates personalized cover letters based on target job role
* Improves professional communication

### Portfolio Builder

Generates portfolio-ready sections:

* About Me
* Skills
* Projects
* Achievements
* Contact Information

### Skill Gap Analyzer (Core AI Feature)

* Compares user skills with industry role requirements
* Calculates job match percentage
* Identifies missing skills
* Recommends improvements

---

## Supported Job Roles

* AI/ML Intern
* Web Developer
* Data Analyst
* IoT Developer
* Software Engineer

---

## Tech Stack

### Frontend

* Streamlit

### Backend

* Python

### Libraries

* PyPDF2
* Pandas

### AI Logic

* NLP-based keyword extraction
* Role-based skill matching
* Recommendation engine

---

## Project Workflow

1. User uploads resume or enters details manually
2. System extracts skills and project details
3. User selects target job role
4. AI compares skills with required industry skills
5. System generates:

   * Resume
   * Cover Letter
   * Portfolio Content
   * Skill Gap Analysis Report

---

## AI Logic Used

### Skill Matching Formula

Match Percentage =
(Number of Matched Skills / Total Required Skills) × 100

Example:

Required Skills: 8
Matched Skills: 5

Match Score = 62.5%

---

## Installation

Clone repository:

```bash
git clone https://github.com/aayushiii18/careerlens_ai.git
cd careerlens_ai
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run application:

```bash
streamlit run app.py
```

---

## Future Improvements

* PDF Resume Download
* ATS Score Checker
* Gemini/OpenAI Integration
* Job Recommendation Engine
* LinkedIn Profile Analyzer
* Advanced NLP Skill Extraction

---

## Use Cases

* Students preparing for internships
* Freshers building resumes
* Placement preparation
* Skill gap identification
* Career planning

---

## Project Status

Completed as part of Edunet Internship Project Submission.
