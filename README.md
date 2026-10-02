# AI Career Intelligence Platform

An NLP-powered job recommendation system that analyzes a candidate's resume and recommends relevant job opportunities based on skills, resume-job similarity, experience compatibility, and job seniority.

## Problem

Job seekers often have to manually compare their resume with hundreds of job postings to determine which roles are relevant and which skills they are missing.

This project automates that process by:

- Extracting skills from a resume PDF
- Comparing candidate skills with job requirements
- Measuring resume-job text similarity
- Considering experience requirements
- Considering job seniority
- Ranking relevant job opportunities
- Identifying matched skills and skill gaps
- Providing an interactive Streamlit dashboard

## How It Works
```text
Resume PDF
    ↓
Resume Text Extraction
    ↓
Skill Extraction
    ↓
Candidate Skill Profile
    ↓
        ┌──────────────────────┐
        │      Job Dataset     │
        │      23K+ Jobs       │
        └──────────────────────┘
                  ↓
        ┌──────────────────────┐
        │   Skill Similarity   │
        ├──────────────────────┤
        │   Text Similarity    │
        ├──────────────────────┤
        │ Experience Matching  │
        ├──────────────────────┤
        │ Seniority Matching   │
        └──────────────────────┘
                  ↓
          Final Match Score
                  ↓
       Top Job Recommendations
                  ↓
       Skill Gaps + Explanation
```

## Key Features

### Resume Analysis
- PDF text extraction using PyMuPDF
- Automated skill extraction
- Skill normalization and alias handling
- Candidate skill profile generation

## Job Recommendation
The recommendation system combines multiple signals:
- Skill similarity
- Resume-job text similarity using TF-IDF
- Experience compatibility
- Job seniority compatibility

The current MVP uses the following weighted scoring approach:

Final Score =50% Skill Similarity + 30% Text Similarity +  5% Experience Compatibility + 15% Seniority Compatibility

## Explainable Recommendations
For each recommended job, the platform displays:
- Match score
- Company
- Work mode
- Salary when disclosed
- Experience requirement
- Matched skills
- Skill gaps

## Interactive Dashboard
The Streamlit dashboard provides:
- Number of jobs analyzed
- Number of detected candidate skills
- Top match score
- Match score visualization
- Work mode distribution
- Most in-demand skills
- Work mode filtering
- Minimum match score filtering

## Dataset
The project uses a job-posting dataset containing 23,000+ job records.
The dataset was cleaned and processed to extract information including:
- Job title
- Company
- Location
- Role category
- Experience range
- Required skills
- Job description
- Work mode
- Salary information

## Machine Learning / NLP

### Skill Representation
- Job skills are converted into a multi-label binary representation using MultiLabelBinarizer.
- The resulting high-dimensional skill matrix is stored using a sparse representation to reduce memory and storage requirements.

### Text Similarity
- TF-IDF with unigrams and bigrams is used to represent job descriptions and resume text.
- Cosine similarity is then used to measure the similarity between the candidate resume and each job.

## Tech Stack

### Programming
- Python

### Machine Learning / NLP
- Scikit-learn
- TF-IDF
- Cosine Similarity
- MultiLabelBinarizer

### Data Processing
- Pandas
- NumPy

### PDF Processing
- PyMuPDF

### Application
- Streamlit

### Model Storage
- Joblib
- SciPy sparse matrices

## Project Structure
```text
project1-career-intelligence/
│
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── data/
│   ├── common_skills.json
│   └── jobs.csv
│
├── docs/
│   ├── challenges.md
│   ├── data-dictionary.md
│   ├── dataset-analysis.md
│   └── project-definition-and-updates.md
│
├── models/
│   ├── mlb.pkl
│   ├── processed_data.pkl
│   ├── skill_matrix_sparse.pkl
│   ├── tfidf.pkl
│   └── tfidf_matrix.pkl
│
├── notebooks/
│   └── 01_data_understanding.ipynb
│
└── src/
    └── resume_parser.py
```

## Installation

### Clone the repository:
```bash
git clone <https://github.com/dipseek/Career-Intelligence-Platform.git>
```

### Install dependencies:
```bash
pip install -r requirements.txt
```

### Run the application:
```bash
streamlit run app.py
```

Then upload a resume PDF through the application.

## Future Improvements

Potential improvements for future versions include:

- Sentence-transformer embeddings for semantic similarity
- Improved resume information extraction
- Better experience extraction from resumes
- Personalized job preferences
- Location preference matching
- Salary preference matching
- Skill importance weighting
- More advanced recommendation models
- User feedback-based recommendation improvement
- Job application tracking

## Project Status

Current status: MVP completed

The current version supports resume parsing, job matching, recommendation ranking, skill-gap analysis, explainability, filtering, and an interactive Streamlit dashboard.