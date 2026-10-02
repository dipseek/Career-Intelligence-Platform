**AI CAREER INTELLIGENCE PLATFORM**

1. What problem does the platform solve?
-> AI Career Intelligence platform would solve the problem of manual searching of jobs and still not getting accurate jobs according to the candidate skills with respect to job descriptions. Also it would help people to find jobs faster and more precisely and it would also recommend what skills have to be prepared for for the particular job.

2. Who is the target user?
-> The target user will be students, fresh graduates, early career job seekers etc.

3. What does the user provide as input?
-> Uploaded information:
Resume/CV

User preferences:
Target role
Location preference
Work mode
Employment type

4. What should the system return?
-> Career Profile
    ↓
Skill Analysis
    ↓
Job Matching
    ↓
Skill Gap
    ↓
Recommendations

5. Why would someone use this instead of simply asking ChatGPT for career advice?
-> Because it gives more accurate answers like it will give you directly the job where you can easily apply and since it would be made just for this purpose so it will serves you better.


6. ML
Machine Learning
machine-learning
MachineLearning

Should my system treat these different or same, if same how?

skill alias → canonical skill normalization



                    USER RESUME
                        │
          ┌─────────────┼─────────────┐
          ↓             ↓             ↓
       Skills         Text       Preferences
          │             │             │
          ↓             ↓             ↓
    Skill Match    Semantic Match   Filters
          │             │             │
          └─────────────┼─────────────┘
                        ↓
                  FINAL MATCH SCORE
                        ↓
                 TOP JOBS



| Component           | What it measures                                                 |
| ------------------- | ---------------------------------------------------------------- |
| `skill_match_score` | How many/strongly the candidate's skills overlap with job skills |
| `text_score`        | How similar the actual resume language is to the job description |


## Before combining them, we'll use sensible weights:
Skill match       50%
Text similarity   30%
Experience        20%
-----------------------
Total             100%


## Skill Gap Analysis

The idea is simple:

What skills does the job require that the candidate doesn't have?

For example:

Candidate:
Python, SQL, Power BI, AWS, Docker

Job requires:
Python, SQL, Tableau, AWS, Spark

→ Matched: Python, SQL, AWS
→ Missing: Tableau, Spark


## status

Component	                      Status
Skill matching	                  ✅
Resume ↔ Job text similarity	  ✅
Experience compatibility	      ✅
Seniority compatibility	          ✅
Final match score	              ✅
Top job recommendations	          ✅
Skill-gap analysis	              ✅
Explainability	                  ✅

# pipeline 
Resume PDF → Skills → 23K jobs → Skill match + Text similarity + Experience → Final score → Top jobs → Skill gaps → Explanation

# streamlit dashboard integrating the whole pipeline into one app.