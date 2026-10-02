import streamlit as st
import pymupdf
import re
import json
import joblib
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# page configuration
st.set_page_config(
    page_title="AI Career Intelligence Platform",
    page_icon="💼",
    layout="wide"
)

# load pickle files
tfidf=joblib.load("models/tfidf.pkl")
mlb=joblib.load("models/mlb.pkl")
processed_data=joblib.load("models/processed_data.pkl")
skill_matrix = joblib.load("models/skill_matrix_sparse.pkl")
tfidf_matrix = joblib.load("models/tfidf_matrix.pkl")

# common skills
with open("data/common_skills.json", "r") as f:
    common_skills = json.load(f)

# layout
st.title("AI Career Intelligence Platform")
st.write("Upload your resume and discover jobs that match your skills and experience.")


uploaded_file=st.file_uploader("Upload your Resume", type=["pdf"])

if uploaded_file:

    # Extract text from PDF
    document = pymupdf.open(stream=uploaded_file.read(), filetype="pdf")

    resume_text = ""

    for page in document:
        resume_text += page.get_text()

    document.close()

    st.success("Resume uploaded successfully!")

    # Show extracted text
    with st.expander("View extracted resume text"):
        st.write(resume_text)


    resume_text_lower = resume_text.lower()


    # -----------------------------
    # Skill cleaning rules
    # -----------------------------

    skill_blacklist = {
        "data",
        "analysis",
        "bi",
        "training",
        "programming",
        "engineering",
        "machine",
        "science",
        "technical",
        "tools",
        "hiring",
        "internship",
        "technology",
        "system",
        "computer",
        "time",
        "education",
        "access",
        "engagement",
        "portfolio",
        "com",
        "insurance",
        "dashboards",
        "integration",
        "linkedin",
        "evaluation",
        "visualization",
        "gui",
        "api",
        "api integration",
        "data science"
    }


    candidate_skill_aliases = {
        "dl": "deep learning",
        "power bi dashboards": "power bi",
        "containerization": "docker"
    }


    # -----------------------------
    # Extract candidate skills
    # -----------------------------

    candidate_skills = []


    for skill in common_skills:

        skill = skill.lower().strip()

        if skill in skill_blacklist:
            continue

        pattern = rf"\b{re.escape(skill)}\b"

        if re.search(pattern, resume_text_lower):

            normalized_skill = candidate_skill_aliases.get(
                skill,
                skill
            )

            candidate_skills.append(
                normalized_skill
            )


    candidate_skills = list(
        dict.fromkeys(candidate_skills)
    )


    # -----------------------------
    # Remove shorter duplicate skills
    # -----------------------------

    filtered_skills = []

    for skill in candidate_skills:

        is_part_of_longer_skill = any(
            skill != other_skill
            and skill in other_skill
            for other_skill in candidate_skills
        )

        if not is_part_of_longer_skill:
            filtered_skills.append(skill)


    candidate_skills = filtered_skills


    # Keep only skills known by trained vocabulary

    candidate_skills = [
        skill
        for skill in candidate_skills
        if skill in mlb.classes_
    ]

    st.subheader("Detected Skills")



    if candidate_skills:
        st.write(", ".join(candidate_skills))
    else:
        st.warning("No skills detected.")


    # calculate skill matching
    candidate_vector=mlb.transform([candidate_skills])

    skill_scores=cosine_similarity(
        candidate_vector,
        skill_matrix
    ).flatten()

    # calculate text similarity
    candidate_tfidf = tfidf.transform([resume_text])

    text_scores = cosine_similarity(
        candidate_tfidf,
        tfidf_matrix
    ).flatten()

    #add experience score
    candidate_experience=0
    experience_scores=(1-processed_data["experience_min_yrs"]/5).clip(0,1)

    #add seniority score
    def seniority_score(job_title):

        title = job_title.lower()

        if any(word in title for word in [
            "senior", "sr.", "lead", "manager",
            "principal", "director", "head"
        ]):
            return 0.2

        elif any(word in title for word in [
            "intern", "trainee", "junior",
            "associate", "fresher"
        ]):
            return 1.0

        else:
            return 0.8

    seniority_scores = (
        processed_data["job_title"]
        .fillna("")
        .apply(seniority_score)
    )

    final_scores = (
        0.50 * skill_scores
        + 0.30 * text_scores
        + 0.05 * experience_scores
        + 0.15 * seniority_scores
    )

    processed_data["final_match_score"] = final_scores


    # -----------------------------
    # Job Filters
    # -----------------------------

    st.subheader("Filter Jobs")

    col1, col2 = st.columns(2)

    with col1:

        work_mode_filter = st.multiselect(
            "Work Mode",
            options=sorted(
                processed_data["work_mode"]
                .dropna()
                .unique()
            ),
            default=sorted(
                processed_data["work_mode"]
                .dropna()
                .unique()
            )
        )

    with col2:

        min_match_score = st.slider(
            "Minimum Match Score",
            min_value=0,
            max_value=100,
            value=0,
            step=5
        )


    filtered_jobs = processed_data[
        processed_data["work_mode"].isin(work_mode_filter)
        &
        (processed_data["final_match_score"] * 100 >= min_match_score)
    ]


    top_jobs = filtered_jobs.nlargest(
        10,
        "final_match_score"
    ).copy()

    if top_jobs.empty:

        st.warning(
            "No jobs match your selected filters. "
            "Try lowering the minimum match score or selecting more work modes."
        )

        st.stop()


    # -----------------------------
    # Skill gaps
    # -----------------------------

    candidate_skill_set = set(candidate_skills)


    def get_skill_gap(job_skills):

        job_skill_set = set(job_skills)

        matched = job_skill_set & candidate_skill_set
        missing = job_skill_set - candidate_skill_set

        return sorted(matched), sorted(missing)


    matched_skills_list = []
    missing_skills_list = []


    for _, row in top_jobs.iterrows():

        matched, missing = get_skill_gap(
            row["skills_filtered"]
        )

        matched_skills_list.append(matched)
        missing_skills_list.append(missing)


    top_jobs["matched_skills"] = matched_skills_list
    top_jobs["missing_skills"] = missing_skills_list


    # -----------------------------
    # Dashboard
    # -----------------------------

    st.subheader("Career Match Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Jobs Analyzed",
            f"{len(processed_data):,}"
        )

    with col2:
        st.metric(
            "Skills Detected",
            len(candidate_skills)
        )

    with col3:

        if len(top_jobs) > 0:

            st.metric(
                "Top Match",
                f"{top_jobs.iloc[0]['final_match_score'] * 100:.1f}%"
            )

        else:

            st.metric(
                "Top Match",
                "No matches"
            )

    # -----------------------------
    # Match Score Chart
    # -----------------------------

    st.subheader("Match Score Overview")

    chart_data = top_jobs[
    ["job_title", "company_name", "final_match_score"]
    ].copy()

    chart_data["final_match_score"] = (
        chart_data["final_match_score"] * 100
    )

    chart_data["job_label"] = [
        f"{i+1}. {title}"
        for i, title in enumerate(chart_data["job_title"])
    ]

    chart_data = chart_data.set_index("job_label")

    st.bar_chart(
        chart_data["final_match_score"]
    )

    st.subheader("Top Job Recommendations")


    # -----------------------------
    # Display recommendations
    # -----------------------------

    for _, row in top_jobs.iterrows():

        st.markdown("---")

        st.markdown(
            f"### {row['job_title']}"
        )

        st.write(
            f"**Company:** {row['company_name']}"
        )

        st.write(
            f"**Work Mode:** {row['work_mode']}"
        )

        # Salary information

        if row["salary_disclosed"]:

            st.write(
                f"**Salary:** ₹{row['salary_min_lpa']:.1f} - "
                f"₹{row['salary_max_lpa']:.1f} LPA"
            )

        else:

            st.write(
                "**Salary:** Not disclosed"
            )


        # Experience explanation

        if candidate_experience < row["experience_min_yrs"]:

            experience_message = (
                f"⚠️ Job requires "
                f"{row['experience_min_yrs']:.0f}-"
                f"{row['experience_max_yrs']:.0f} years; "
                f"candidate has {candidate_experience} years."
            )

        elif candidate_experience > row["experience_max_yrs"]:

            experience_message = (
                f"ℹ️ Candidate has more experience than "
                f"the stated "
                f"{row['experience_min_yrs']:.0f}-"
                f"{row['experience_max_yrs']:.0f} year range."
            )

        else:

            experience_message = (
                f"✅ Candidate experience matches the "
                f"{row['experience_min_yrs']:.0f}-"
                f"{row['experience_max_yrs']:.0f} year requirement."
            )


        st.write(
            f"**Experience:** {experience_message}"
        )


        st.metric(
            "Match Score",
            f"{row['final_match_score'] * 100:.1f}%"
        )


        col1, col2 = st.columns(2)


        with col1:

            st.write("✅ **Matched Skills**")

            if row["matched_skills"]:

                st.write(
                    ", ".join(row["matched_skills"])
                )

            else:

                st.write(
                    "No direct skill matches found."
                )


        with col2:

            st.write("❌ **Skill Gaps**")

            if row["missing_skills"]:

                st.write(
                    ", ".join(row["missing_skills"])
                )

            else:

                st.write(
                    "No major skill gaps detected."
                )


        st.info(
            "This recommendation is based on "
            "skill similarity, resume-job text similarity, "
            "experience compatibility, and job seniority."
        )



    # -----------------------------
    # Work Mode Distribution
    # -----------------------------

    st.subheader("Job Work Mode Distribution")

    work_mode_counts = (
        processed_data["work_mode"]
        .value_counts()
    )

    st.bar_chart(work_mode_counts)


    # -----------------------------
    # Most Common Skills in Jobs
    # -----------------------------

    st.subheader("Most In-Demand Skills")

    all_job_skills = []

    for skills in top_jobs["skills_filtered"]:
        all_job_skills.extend(skills)

    skill_counts = (
        pd.Series(all_job_skills)
        .value_counts()
        .head(10)
    )

    st.bar_chart(skill_counts)
