import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv
from agent import JobSearchAgent
from utils.database import init_db, save_job, get_saved_jobs, delete_job
import json

# Load .env from utils directory
env_path = Path(__file__).parent / "utils" / ".env"
load_dotenv(env_path)

# Page config
st.set_page_config(
    page_title="AI Career Agent",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .feature-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #667eea;
    }
    .success-box {
        background-color: #d4edda;
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #28a745;
        margin: 10px 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #ffc107;
        margin: 10px 0;
    }
    .info-box {
        background-color: #d1ecf1;
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #17a2b8;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent" not in st.session_state:
    st.session_state.agent = None
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
if "job_desc_text" not in st.session_state:
    st.session_state.job_desc_text = ""

# Load API key from env (no user input needed)
api_key = os.getenv("GROQ_API_KEY", "")
if not api_key:
    st.error("❌ API Key not found in .env file. Please add GROQ_API_KEY to utils/.env")
    st.stop()

# Initialize agent
if st.session_state.agent is None:
    st.session_state.agent = JobSearchAgent(api_key)

init_db()

# ============== SIDEBAR ==============
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/briefcase.png", width=80)
    st.title("🚀 Career Agent")
    st.markdown("**Your personal AI job search assistant**")
    st.markdown("---")
    
    # Navigation
    st.subheader("📍 Navigation")
    page = st.radio(
        "Choose a feature:",
        ["🏠 Home", "🔍 Job Search", "🛣️ Career Roadmap", 
         "🎤 Mock Interview", "📚 Learning Path", "💡 Recommendations", 
         "📱 Application Tracker", "📄 Resume Analyzer"],
        key="nav"
    )
    
    st.markdown("---")
    st.caption("✨ Build your career with AI assistance")


# ============== PAGE ROUTING ==============

# HOME PAGE
if page == "🏠 Home":
    st.markdown('<div class="main-header">🚀 Welcome to Your AI Career Agent</div>', unsafe_allow_html=True)
    st.markdown("Your personal AI-powered career assistant for job search, interview prep, and career growth.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 What Can I Do?
        
        **Job Search**
        - Find jobs matching your skills
        - Filter by location, salary, experience
        
        **Interview Prep**
        - Mock interview questions
        - Company research
        - Interview tips & strategies
        
        **Career Growth**
        - Personalized learning paths
        - Course recommendations
        - Skill development roadmaps
        """)
    
    with col2:
        st.markdown("""
        ### ⭐ Key Features
        
        **️ Career Roadmap**: Step-by-step learning plan
        - Domain-specific paths
        - Timeline & milestones
        
        **📱 Application Tracker**: Track all applications
        - Status updates
        - Follow-up reminders
        
        **💡 Personalized Advice**: Get actionable insights
        - Based on your profile
        - Industry trends
        """)
    
    st.markdown("---")
    st.markdown("### 🌟 Quick Tips for Job Hunters")
    st.info("""
    ✅ **Prepare:** Update resume, practice interviews, learn trending skills\n
    ✅ **Network:** Connect with 5 people on LinkedIn daily\n
    ✅ **Apply:** Target 20-30 relevant positions\n
    ✅ **Follow-up:** Track applications, follow up after 1 week\n
    ✅ **Learn:** Upskill continuously, take certifications
    """)

# JOB SEARCH PAGE
elif page == "🔍 Job Search":
    st.header("🔍 Find Your Dream Job")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        role = st.text_input("Job Role", placeholder="e.g., Python Developer", key="job_role")
    with col2:
        city = st.selectbox("City", ["Bangalore", "Mumbai", "Hyderabad", "Pune", "Delhi", "Chennai", "Remote"], key="job_city")
    with col3:
        exp = st.selectbox("Experience", ["Fresher", "1-3 years", "3-5 years", "5+ years"], key="job_exp")
    with col4:
        salary = st.number_input("Min Salary (LPA)", value=0, key="job_salary")
    
    if st.button("🔎 Search Jobs", use_container_width=True):
        if role:
            query = f"Find {role} jobs in {city} for {exp} experience"
            if salary > 0:
                query += f" with minimum {salary} LPA salary"
            
            with st.spinner("🔄 Searching for jobs..."):
                response = st.session_state.agent.chat(query, [])
                st.success("✅ Jobs found!")
                st.markdown(response)
        else:
            st.warning("⚠️ Please enter a job role!")

# CAREER ROADMAP PAGE
elif page == "🛣️ Career Roadmap":
    st.header("🛣️ Career Development Roadmap")
    
    col1, col2 = st.columns(2)
    
    with col1:
        domain = st.selectbox(
            "Select Your Domain",
            ["Python Developer", "Data Scientist", "React Developer", "DevOps Engineer", "Java Developer", "Other"],
            key="roadmap_domain"
        )
    
    with col2:
        level = st.selectbox(
            "Current Level",
            ["Fresher", "1-3 years", "3-5 years", "5+ years"],
            key="roadmap_level"
        )
    
    if st.button("📚 Get Roadmap", use_container_width=True):
        with st.spinner("🔄 Generating roadmap..."):
            query = f"Create a detailed career roadmap for {domain} at {level} level"
            response = st.session_state.agent.chat(query, [])
            st.markdown(response)

# MOCK INTERVIEW PAGE
elif page == "🎤 Mock Interview":
    st.header("🎤 Practice Mock Interview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        role = st.selectbox(
            "Select Role",
            ["Python Developer", "Data Scientist", "React Developer", "DevOps Engineer", "Java Developer"],
            key="interview_role"
        )
    
    with col2:
        round_type = st.selectbox(
            "Interview Round",
            ["Technical", "Manager/Behavioral", "HR"],
            key="interview_round"
        )
    
    if st.button("🎯 Get Interview Questions", use_container_width=True):
        with st.spinner("🔄 Preparing questions..."):
            query = f"Give me mock interview questions for {role} {round_type} round"
            response = st.session_state.agent.chat(query, [])
            
            st.markdown("### 🎤 Interview Questions")
            st.markdown(response)
            
            st.markdown("---")
            st.subheader("💡 Interview Tips")
            st.info("""
            • Take 15-20 seconds to think before answering
            • Use the STAR method for behavioral questions
            • Ask clarifying questions if needed
            • Provide specific examples
            • Show your problem-solving approach
            • Prepare counter-questions for the interviewer
            """)

# LEARNING PATH PAGE
elif page == "📚 Learning Path":
    st.header("📚 Personalized Learning Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        skill = st.text_input("Skill to Learn", placeholder="e.g., Python, React, Data Science", key="learn_skill")
    
    with col2:
        timeline = st.select_slider("Timeline", ["1 month", "3 months", "6 months", "12 months"], value="3 months", key="learn_timeline")
    
    if st.button("📖 Get Recommendations", use_container_width=True):
        if skill:
            with st.spinner("🔄 Finding courses..."):
                query = f"Recommend courses, certificates, and projects to learn {skill} in {timeline}"
                response = st.session_state.agent.chat(query, [])
                st.markdown(response)
        else:
            st.warning("⚠️ Please enter a skill!")

# PERSONALIZED RECOMMENDATIONS PAGE
elif page == "💡 Recommendations":
    st.header("💡 Your Personalized Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        exp = st.selectbox(
            "Your Experience Level",
            ["Fresher", "1-3 years", "3-5 years", "5+ years"],
            key="rec_exp"
        )
    
    with col2:
        interests = st.text_input("Your Tech Interests", placeholder="e.g., AI, Cloud, Web Dev", key="rec_interests")
    
    if st.button("🎯 Get Personalized Advice", use_container_width=True):
        with st.spinner("🔄 Generating recommendations..."):
            query = f"Give me personalized recommendations for someone with {exp} experience interested in {interests or 'tech'}"
            response = st.session_state.agent.chat(query, [])
            st.markdown(response)

# APPLICATION TRACKER PAGE
elif page == "📱 Application Tracker":
    st.header("📱 Track Your Job Applications")
    
    tab1, tab2 = st.tabs(["📊 View Applications", "➕ Add New Application"])
    
    with tab1:
        jobs = get_saved_jobs()
        
        if jobs:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader("Your Applications")
            with col2:
                if st.button("🔄 Refresh", use_container_width=True):
                    st.rerun()
            
            # Status breakdown
            status_counts = {}
            for job in jobs:
                status = job[5]
                status_counts[status] = status_counts.get(status, 0) + 1
            
            cols = st.columns(len(status_counts) + 1)
            for i, (status, count) in enumerate(status_counts.items()):
                with cols[i]:
                    st.metric(status, count)
            
            st.markdown("---")
            
            # Display jobs
            status_colors = {
                "Applied": "🔵",
                "Shortlisted": "🟡",
                "Interview": "🟠",
                "Rejected": "🔴",
                "Offered": "🟢",
            }
            
            for job in jobs:
                id_, title, company, location, salary, status, link, date = job
                with st.container(border=True):
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.markdown(f"### **{title}** @ **{company}**")
                        st.caption(f"📍 {location or 'N/A'} | 💰 {salary or 'N/A'} LPA | 📅 {date[:10]}")
                        if link:
                            st.markdown(f"[🔗 View Job]({link})")
                    
                    with col2:
                        new_status = st.selectbox(
                            "Status",
                            ["Applied", "Shortlisted", "Interview", "Rejected", "Offered"],
                            index=["Applied", "Shortlisted", "Interview", "Rejected", "Offered"].index(status),
                            key=f"status_{id_}"
                        )
                        if new_status != status:
                            st.success(f"✅ Status updated to {new_status}")
                    
                    with col3:
                        if st.button("🗑️ Delete", key=f"del_{id_}", use_container_width=True):
                            delete_job(id_)
                            st.success("Deleted!")
                            st.rerun()
        else:
            st.info("📭 No applications tracked yet. Add one below!")
    
    with tab2:
        st.subheader("Add New Application")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            title = st.text_input("Job Title")
        with col2:
            company = st.text_input("Company")
        with col3:
            location = st.text_input("Location")
        
        col4, col5, col6 = st.columns(3)
        with col4:
            salary = st.text_input("Salary (LPA)")
        with col5:
            status = st.selectbox("Status", ["Applied", "Shortlisted", "Interview", "Rejected", "Offered"])
        with col6:
            link = st.text_input("Job Link")
        
        if st.button("💾 Save Application", use_container_width=True):
            if title and company:
                save_job(title, company, location, salary, status, link)
                st.success("✅ Application saved!")
                st.rerun()
            else:
                st.warning("⚠️ Please enter job title and company!")

# RESUME ANALYZER PAGE
elif page == "📄 Resume Analyzer":
    st.header("📄 AI Resume Analyzer")
    
    st.markdown("Get AI-powered feedback to optimize your resume for ATS and improve your match score with job descriptions.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Your Resume")
        resume_text = st.text_area("Paste your resume text:", height=350, key="analyzer_resume")
    
    with col2:
        st.subheader("📋 Target Job Description")
        job_desc = st.text_area("(Optional) Paste target job description:", height=350, key="analyzer_jd")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 Analyze Resume", use_container_width=True):
            if resume_text:
                with st.spinner("🔄 Analyzing resume..."):
                    prompt = f"""Analyze this resume and provide:
1. **ATS Score** (out of 100) - How well it will pass through ATS systems
2. **Key Strengths** - What's good about this resume
3. **Areas to Improve** - What needs work
4. **Missing Elements** - What should be added
5. **Formatting Issues** - Any ATS-unfriendly formatting
6. **Top 3 Recommendations** - Specific actions to improve

RESUME:
{resume_text}

{"JOB DESCRIPTION:" + job_desc if job_desc else ""}

Provide detailed, actionable feedback."""
                    response = st.session_state.agent.chat(prompt, [])
                    st.markdown(response)
            else:
                st.warning("⚠️ Please paste your resume!")
    
    with col2:
        if st.button("📊 Check Job Match", use_container_width=True):
            if resume_text and job_desc:
                with st.spinner("🔄 Calculating match..."):
                    query = f"Resume:\n{resume_text}\n\nJob Description:\n{job_desc}\n\nProvide a detailed match analysis"
                    response = st.session_state.agent.chat(query, [])
                    st.markdown(response)
            else:
                st.warning("⚠️ Please paste both resume and job description!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>🚀 <strong>AI Career Agent</strong> | Your personal AI-powered career assistant</p>
    <p>Made with ❤️ to help you land your dream job</p>
</div>
""", unsafe_allow_html=True)