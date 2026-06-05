import re

def search_jobs_tool(role: str, location: str = "Any", experience: str = "Any", skills: str = "", salary_min: str = "0"):
    """
    Search for job opportunities in the Indian market.
    
    Args:
        role: The job role or title (e.g., 'Python Developer', 'Data Scientist').
        location: The city in India (e.g., 'Bangalore', 'Remote'). Defaults to 'Any'.
        experience: Experience level (e.g., 'Fresher', '2 years', '5+ years'). Defaults to 'Any'.
        skills: Comma-separated list of required skills.
        salary_min: Minimum expected salary in LPA (e.g., '10').
    """
    role_lower = role.lower()

    MOCK_JOBS = {
        "python": [
            {"title": "Python Developer", "company": "Razorpay", "location": "Bangalore", "salary": "12-20 LPA", "exp": "2-4 years", "skills": "Python, Django, REST APIs, SQL", "type": "Product"},
            {"title": "Python Backend Engineer", "company": "CRED", "location": "Bangalore", "salary": "15-25 LPA", "exp": "3-6 years", "skills": "Python, FastAPI, PostgreSQL, Redis", "type": "Startup"},
            {"title": "Python Developer", "company": "Infosys", "location": "Multiple", "salary": "6-12 LPA", "exp": "1-3 years", "skills": "Python, Django, REST APIs", "type": "Service"},
            {"title": "Python Fresher", "company": "TCS", "location": "Multiple", "salary": "3.36 LPA", "exp": "Fresher", "skills": "Python, SQL, Problem Solving", "type": "Service"},
            {"title": "Sr. Python Developer", "company": "Meesho", "location": "Bangalore", "salary": "20-35 LPA", "exp": "4-7 years", "skills": "Python, Microservices, AWS, Kafka", "type": "Startup"},
        ],
        "data scientist": [
            {"title": "Data Scientist", "company": "Flipkart", "location": "Bangalore", "salary": "18-30 LPA", "exp": "2-5 years", "skills": "Python, ML, SQL, Statistics", "type": "Product"},
            {"title": "Junior Data Scientist", "company": "Mu Sigma", "location": "Bangalore", "salary": "5-10 LPA", "exp": "Fresher", "skills": "Python, R, Statistics, ML", "type": "Analytics"},
            {"title": "Data Scientist", "company": "PhonePe", "location": "Bangalore", "salary": "15-28 LPA", "exp": "2-4 years", "skills": "Python, TensorFlow, SQL, A/B Testing", "type": "Fintech"},
            {"title": "ML Engineer", "company": "Amazon", "location": "Hyderabad", "salary": "25-45 LPA", "exp": "3-6 years", "skills": "Python, ML, Deep Learning, AWS SageMaker", "type": "Big Tech"},
        ],
        "react": [
            {"title": "React Developer", "company": "Swiggy", "location": "Bangalore", "salary": "12-22 LPA", "exp": "2-4 years", "skills": "React, TypeScript, Redux, Node.js", "type": "Startup"},
            {"title": "Frontend Developer", "company": "Paytm", "location": "Noida", "salary": "10-18 LPA", "exp": "1-3 years", "skills": "React, JavaScript, CSS, HTML5", "type": "Fintech"},
            {"title": "React Fresher", "company": "Capgemini", "location": "Multiple", "salary": "4-7 LPA", "exp": "Fresher", "skills": "React, JavaScript, HTML, CSS", "type": "Service"},
            {"title": "Sr. React Engineer", "company": "Groww", "location": "Bangalore", "salary": "18-32 LPA", "exp": "4-7 years", "skills": "React, TypeScript, GraphQL", "type": "Fintech"},
        ],
        "java": [
            {"title": "Java Developer", "company": "Wipro", "location": "Multiple", "salary": "5-12 LPA", "exp": "1-3 years", "skills": "Java, Spring Boot, SQL, REST APIs", "type": "Service"},
            {"title": "Java Backend Engineer", "company": "Ola", "location": "Bangalore", "salary": "14-25 LPA", "exp": "3-5 years", "skills": "Java, Spring Boot, Microservices, Kafka", "type": "Startup"},
            {"title": "Java Fresher", "company": "HCL", "location": "Multiple", "salary": "3.5-6 LPA", "exp": "Fresher", "skills": "Java, OOP, SQL", "type": "Service"},
        ],
        "devops": [
            {"title": "DevOps Engineer", "company": "Freshworks", "location": "Chennai", "salary": "12-22 LPA", "exp": "2-4 years", "skills": "AWS, Docker, Kubernetes, CI/CD", "type": "SaaS"},
            {"title": "Site Reliability Engineer", "company": "Zepto", "location": "Mumbai", "salary": "18-32 LPA", "exp": "3-6 years", "skills": "Kubernetes, Terraform, Python, AWS", "type": "Startup"},
            {"title": "Cloud Engineer", "company": "Accenture", "location": "Multiple", "salary": "8-16 LPA", "exp": "2-5 years", "skills": "AWS/Azure/GCP, Docker, Jenkins", "type": "MNC"},
        ],
        "default": [
            {"title": "Software Engineer", "company": "TCS", "location": "Multiple", "salary": "3.36-7 LPA", "exp": "Fresher", "skills": "Problem Solving, SQL, Any Language", "type": "Service"},
            {"title": "Software Developer", "company": "Infosys", "location": "Multiple", "salary": "6-10 LPA", "exp": "1-2 years", "skills": "Java/Python, SQL, Communication", "type": "Service"},
            {"title": "Associate Engineer", "company": "Cognizant", "location": "Multiple", "salary": "4-8 LPA", "exp": "Fresher-1 year", "skills": "Any Tech Stack, SQL", "type": "Service"},
        ],
    }

    matched = []
    for key in MOCK_JOBS:
        if key in role_lower:
            matched.extend(MOCK_JOBS[key])

    if not matched:
        matched = MOCK_JOBS["default"]

    # Filter by location
    if location and location.lower() not in ("any", "all", ""):
        filtered = [j for j in matched if location.lower() in j["location"].lower() or "multiple" in j["location"].lower()]
        if filtered:
            matched = filtered

    # Filter by skills (Simple keyword matching)
    if skills:
        skill_list = [s.strip().lower() for s in skills.split(",")]
        matched = [j for j in matched if any(s in j["skills"].lower() for s in skill_list)]

    # Filter by experience
    if experience.lower() != "any":
        exp_q_nums = [int(n) for n in re.findall(r'\d+', experience)]
        is_fresher_q = "fresher" in experience.lower()
        
        filtered_exp = []
        for j in matched:
            job_exp_str = j["exp"].lower()
            if is_fresher_q and "fresher" in job_exp_str:
                filtered_exp.append(j)
            elif exp_q_nums:
                job_nums = [int(n) for n in re.findall(r'\d+', job_exp_str)]
                if job_nums:
                    j_min = job_nums[0]
                    j_max = job_nums[-1] if len(job_nums) > 1 else (j_min + 5 if "+" in job_exp_str else j_min)
                    if j_min <= exp_q_nums[0] <= j_max:
                        filtered_exp.append(j)
        matched = filtered_exp

    # Filter by salary_min
    if salary_min and salary_min != "0":
        try:
            min_val = float(re.findall(r'\d+\.?\d*', salary_min)[0])
            matched = [j for j in matched if max([float(n) for n in re.findall(r'\d+\.?\d*', j["salary"])] + [0]) >= min_val]
        except (IndexError, ValueError):
            pass

    result = f"🔍 **Job Search Results for: {role}**\n"
    result += f"📍 Location: {location} | 👤 Experience: {experience}\n\n"
    result += f"Found **{len(matched)} opportunities**:\n\n"

    for i, job in enumerate(matched[:6], 1):
        result += f"**{i}. {job['title']}** — {job['company']}\n"
        result += f"   📍 {job['location']} | 💰 {job['salary']} | 🏢 {job['type']}\n"
        result += f"   ⏱️ Experience: {job['exp']}\n"
        result += f"   🛠️ Skills: {job['skills']}\n"
        result += f"   🔗 Apply: naukri.com\n\n"

    result += "\n📌 **Where to Apply:** Naukri.com | LinkedIn | Indeed India"
    return result


def get_salary_info_tool(role: str, experience: str = "fresher", location: str = "Bangalore", company_type: str = "any"):
    """
    Get salary benchmarks and LPA (Lakhs Per Annum) ranges for specific roles in India.
    
    Args:
        role: The job role to research.
        experience: Years of experience or 'fresher'.
        location: The city for cost-of-living adjustment.
        company_type: Type of company (e.g., 'Product', 'Service', 'Startup').
    """
    SALARY_DATA = {
        "software engineer": {"fresher": (3, 7), "1-3": (6, 14), "3-5": (12, 22), "5+": (20, 45)},
        "python developer": {"fresher": (3, 8), "1-3": (7, 15), "3-5": (13, 25), "5+": (22, 50)},
        "data scientist": {"fresher": (4, 9), "1-3": (8, 18), "3-5": (15, 30), "5+": (25, 60)},
        "data analyst": {"fresher": (3, 6), "1-3": (6, 12), "3-5": (10, 20), "5+": (18, 35)},
        "react developer": {"fresher": (3, 8), "1-3": (7, 16), "3-5": (13, 25), "5+": (22, 45)},
        "java developer": {"fresher": (3, 7), "1-3": (6, 14), "3-5": (12, 22), "5+": (20, 42)},
        "devops engineer": {"fresher": (4, 8), "1-3": (8, 18), "3-5": (15, 30), "5+": (25, 55)},
        "machine learning engineer": {"fresher": (5, 10), "1-3": (10, 22), "3-5": (18, 35), "5+": (30, 70)},
        "default": {"fresher": (3, 6), "1-3": (6, 12), "3-5": (10, 20), "5+": (18, 35)},
    }

    role_lower = role.lower()
    salary_range = None
    for key in SALARY_DATA:
        if key in role_lower:
            salary_range = SALARY_DATA[key]
            break
    if not salary_range:
        salary_range = SALARY_DATA["default"]

    exp_key = "fresher"
    if "+" in experience or "10" in experience or any(x in experience for x in ["6", "7", "8", "9"]):
        exp_key = "5+"
    elif any(x in experience for x in ["4", "5"]):
        exp_key = "3-5"
    elif any(x in experience for x in ["1", "2", "3"]):
        exp_key = "1-3"

    low, high = salary_range.get(exp_key, (4, 10))

    multipliers = {"bangalore": 1.15, "mumbai": 1.1, "hyderabad": 1.05, "pune": 1.0, "delhi": 1.1, "chennai": 0.95}
    mult = multipliers.get(location.lower(), 1.0)
    adj_low = round(low * mult, 1)
    adj_high = round(high * mult, 1)

    result = f"💰 **Salary Benchmark: {role} | {experience} | {location}**\n\n"
    result += f"📊 **Salary Range: {adj_low} – {adj_high} LPA**\n\n"
    result += "**Breakdown by Company Type:**\n"
    result += f"  🏢 IT Services (TCS/Infosys/Wipro): {adj_low} – {round(adj_low*1.3, 1)} LPA\n"
    result += f"  🌐 MNCs (Google/Amazon/Microsoft): {round(adj_low*1.5, 1)} – {adj_high} LPA\n"
    result += f"  🚀 Funded Startups: {round(adj_low*1.2, 1)} – {round(adj_high*0.9, 1)} LPA\n\n"
    result += "**💡 Negotiation Tips:**\n"
    result += "  • Always negotiate — most companies expect it\n"
    result += "  • Ask about Variable Pay, joining bonus, ESOP\n"
    result += "  • CTC vs In-hand: take-home is ~70-75% of CTC\n"
    return result


def get_company_info_tool(company_name: str, info_type: str = "general"):
    """
    Research a specific company's culture, interview process, and reviews.
    
    Args:
        company_name: Name of the company (e.g., 'TCS', 'Flipkart').
        info_type: Specific info needed ('salary', 'interview', 'culture').
    """
    COMPANY_DATA = {
        "tcs": {
            "full_name": "Tata Consultancy Services",
            "type": "IT Services (MNC)", "rating": 3.8, "hq": "Mumbai",
            "fresher_salary": "3.36 - 7 LPA",
            "pros": ["Job security", "Good training", "Global exposure", "Strong brand"],
            "cons": ["Slow growth", "Bond of 2 years", "Repetitive work"],
            "interview": "TCS NQT → Technical → HR",
            "notice_period": "90 days", "bond": "2-year bond for freshers",
            "website": "tcs.com/careers",
        },
        "infosys": {
            "full_name": "Infosys Limited",
            "type": "IT Services (MNC)", "rating": 3.7, "hq": "Bangalore",
            "fresher_salary": "3.6 - 8 LPA",
            "pros": ["Good training", "Stable company", "International projects"],
            "cons": ["Slow appraisals", "Bureaucratic", "Service-based work"],
            "interview": "InfyTQ test → Technical → HR",
            "notice_period": "90 days", "bond": "1-year service agreement",
            "website": "infosys.com/careers",
        },
        "wipro": {
            "full_name": "Wipro Limited",
            "type": "IT Services (MNC)", "rating": 3.6, "hq": "Bangalore",
            "fresher_salary": "3.5 - 7 LPA",
            "pros": ["Good benefits", "Training programs", "Job security"],
            "cons": ["Slow growth", "Bond period"],
            "notice_period": "90 days", "website": "wipro.com/careers",
        },
        "flipkart": {
            "full_name": "Flipkart",
            "type": "E-commerce (Startup)", "rating": 4.1, "hq": "Bangalore",
            "fresher_salary": "12 - 25 LPA",
            "pros": ["High salary", "Great tech stack", "Fast growth", "ESOP"],
            "cons": ["High pressure", "Work-life imbalance"],
            "interview": "Online coding → DSA rounds → System Design → HR",
            "notice_period": "30-60 days", "website": "flipkartcareers.com",
        },
        "google": {
            "full_name": "Google India",
            "type": "Big Tech (MNC)", "rating": 4.5, "hq": "Hyderabad/Bangalore",
            "fresher_salary": "20 - 50 LPA",
            "pros": ["Best compensation", "World-class culture", "Learning opportunities"],
            "cons": ["Extremely competitive hiring", "High performance bar"],
            "interview": "Phone screens → 4-5 technical rounds → HR",
            "notice_period": "60-90 days", "website": "careers.google.com",
        },
        "amazon": {
            "full_name": "Amazon India / AWS",
            "type": "Big Tech (MNC)", "rating": 3.9, "hq": "Hyderabad/Bangalore",
            "fresher_salary": "18 - 40 LPA",
            "pros": ["High comp", "Career growth", "ESOP"],
            "cons": ["Work-life balance challenges", "High pressure"],
            "interview": "OA → 4-5 Loops (DSA + System Design)",
            "notice_period": "90 days", "website": "amazon.jobs",
        },
    }

    key = company_name.lower().strip()
    company = COMPANY_DATA.get(key)

    if company:
        result = f"🏢 **{company.get('full_name', company_name)}**\n"
        result += f"Type: {company.get('type')} | ⭐ {company.get('rating')}/5 | HQ: {company.get('hq')}\n\n"
        result += f"💰 **Fresher Salary:** {company.get('fresher_salary')}\n\n"
        pros = company.get("pros", [])
        cons = company.get("cons", [])
        if pros:
            result += "✅ **Pros:**\n" + "\n".join(f"  • {p}" for p in pros) + "\n\n"
        if cons:
            result += "❌ **Cons:**\n" + "\n".join(f"  • {c}" for c in cons) + "\n\n"
        result += f"🎤 **Interview:** {company.get('interview', 'N/A')}\n"
        result += f"⏰ **Notice Period:** {company.get('notice_period', 'N/A')}\n"
        if company.get("bond"):
            result += f"📋 **Bond:** {company['bond']}\n"
        result += f"🔗 **Apply:** {company.get('website')}\n"
    else:
        result = f"🏢 **{company_name}**\n\n"
        result += "Research this company on:\n"
        result += "  • **AmbitionBox.com** — Indian company reviews\n"
        result += "  • **Glassdoor.com** — Salary + reviews\n"
        result += "  • **LinkedIn** — Employee count and growth\n"

    return result


def get_interview_tips_tool(role: str, company: str = "", round_type: str = "technical", experience_level: str = "fresher"):
    """
    Provide common interview questions and preparation tips for specific roles and companies.
    
    Args:
        role: The target job role.
        company: The company name (optional).
        round_type: Type of interview round ('technical', 'hr', 'managerial').
        experience_level: Level of seniority.
    """
    role_lower = role.lower()

    result = f"🎤 **Interview Prep: {role}**"
    if company:
        result += f" @ {company}"
    result += f" ({round_type.title()} Round)\n\n"

    result += "**📚 Must-Prepare Topics:**\n"
    result += "  🔹 Data Structures: Arrays, LinkedList, Trees, Graphs\n"
    result += "  🔹 Algorithms: Sorting, BFS/DFS, Dynamic Programming\n"
    result += "  🔹 SQL Queries + Joins\n"
    result += "  🔹 OOP Concepts\n\n"

    result += "**❓ Sample Interview Questions:**\n\n"

    if "python" in role_lower:
        questions = [
            "Difference between list and tuple in Python?",
            "Explain Python's GIL (Global Interpreter Lock)",
            "What are decorators and how do you use them?",
            "Difference between shallow and deep copy?",
            "What is the difference between *args and **kwargs?",
            "Explain list comprehensions vs generator expressions",
        ]
    elif "react" in role_lower or "frontend" in role_lower:
        questions = [
            "What is the Virtual DOM and how does React use it?",
            "Explain the difference between useState and useReducer",
            "What are React hooks? List the most used ones.",
            "What is prop drilling and how do you avoid it?",
            "Difference between controlled and uncontrolled components?",
            "How does React.memo() help with performance?",
        ]
    elif "data scientist" in role_lower or "ml" in role_lower:
        questions = [
            "Explain the bias-variance tradeoff",
            "What is overfitting and how do you prevent it?",
            "Difference between L1 and L2 regularization?",
            "When would you use Random Forest vs Gradient Boosting?",
            "How do you handle class imbalance in a dataset?",
            "What is cross-validation and why does it matter?",
        ]
    elif "java" in role_lower:
        questions = [
            "Difference between HashMap and ConcurrentHashMap?",
            "Explain Java memory model (Stack vs Heap)",
            "What are the SOLID principles?",
            "Explain Spring Boot's dependency injection",
            "What is the difference between abstract class and interface?",
        ]
    else:
        questions = [
            "Tell me about yourself",
            "What is your greatest technical strength?",
            "Describe a challenging project you worked on",
            "Where do you see yourself in 5 years?",
            "Why do you want to join this company?",
        ]

    for i, q in enumerate(questions, 1):
        result += f"  {i}. {q}\n"

    result += "\n**💡 Tips:**\n"
    result += "  ✅ Practice on LeetCode (Easy/Medium)\n"
    result += "  ✅ Know your resume projects very well\n"
    result += "  ✅ Prepare STAR format answers for HR\n"
    result += "  ✅ Research the company before interview\n"
    result += "  ✅ Always negotiate salary after offer\n"

    return result


def get_indian_job_market_tool(sector: str, query_type: str = "trends"):
    """
    Get overall trends and insights about the Indian job market for specific sectors.
    
    Args:
        sector: The industry sector (e.g., 'IT', 'Finance').
        query_type: Type of insight ('trends', 'skills', 'cities').
    """
    sector_lower = sector.lower()

    result = f"📊 **Indian Job Market Insights: {sector.title()}**\n\n"

    if any(k in sector_lower for k in ["it", "tech", "software"]):
        result += "**🔥 Hot Skills (2024-25):**\n"
        result += "  1. AI/ML & Generative AI (Highest demand!)\n"
        result += "  2. Cloud (AWS, Azure, GCP)\n"
        result += "  3. DevOps / Kubernetes / Docker\n"
        result += "  4. React.js + TypeScript\n"
        result += "  5. Python (Backend + Data)\n"
        result += "  6. Cybersecurity\n\n"
        result += "**🏆 Top Companies Hiring:**\n"
        result += "  🔵 Services: TCS, Infosys, Wipro, HCL, Cognizant\n"
        result += "  🟢 Product: Google, Microsoft, Amazon, Flipkart\n"
        result += "  🟡 Startups: Zepto, Meesho, PhonePe, CRED, Groww\n\n"
        result += "**📍 Top Tech Cities:**\n"
        result += "  1. Bangalore — Silicon Valley of India\n"
        result += "  2. Hyderabad — IT + MNCs\n"
        result += "  3. Pune — IT + Auto\n"
        result += "  4. Delhi NCR — MNCs + Fintech\n"
        result += "  5. Mumbai — Finance + Startups\n"
    else:
        result += f"**📈 Key Trends in {sector}:**\n"
        result += "  • Growing job market with digitization\n"
        result += "  • Remote/hybrid work expanding\n"
        result += "  • Skill-based hiring increasing\n\n"
        result += "Check Naukri.com and LinkedIn for latest openings."

    return result


def calculate_match_score(resume_text: str, job_desc: str) -> str:
    """
    Calculate match score between resume and job description.
    
    Args:
        resume_text: Resume content
        job_desc: Job description
    """
    result = "📊 **Resume-Job Match Score Analysis**\n\n"
    
    resume_lower = resume_text.lower()
    job_lower = job_desc.lower()
    
    skills_keywords = ["python", "java", "javascript", "react", "aws", "docker", "kubernetes", "sql", "mongodb", "django", "flask", "spring", "node.js", "typescript", "devops", "ci/cd"]
    matched_skills = [s for s in skills_keywords if s in resume_lower and s in job_lower]
    
    score = min(95, 40 + len(matched_skills) * 8)
    
    result += f"## 🎯 Overall Match Score: **{score}/100**\n\n"
    
    if score >= 80:
        result += "✅ **Excellent Match!** You're a great fit for this role.\n\n"
    elif score >= 60:
        result += "🟡 **Good Match.** You have most required skills. Work on missing ones.\n\n"
    else:
        result += "🔴 **Partial Match.** Consider upskilling before applying.\n\n"
    
    result += f"**🎯 Matched Skills ({len(matched_skills)}):**\n"
    result += " • " + "\n • ".join(matched_skills) if matched_skills else "None found"
    result += "\n\n"
    
    missing = [s for s in skills_keywords if s in job_lower and s not in resume_lower]
    result += f"**⚠️ Missing Skills ({len(missing)}):**\n"
    result += " • " + "\n • ".join(missing[:5]) if missing else "All covered!"
    result += "\n\n"
    
    result += "**💡 Recommendations:**\n"
    result += "  1. Highlight matched skills in resume\n"
    result += "  2. Add projects demonstrating top 3 missing skills\n"
    result += "  3. Get certifications for key missing skills\n"
    result += "  4. Customize cover letter to match JD\n"
    
    return result


def get_career_roadmap(domain: str, experience_level: str = "fresher") -> str:
    """
    Provide learning roadmap for career progression in a domain.
    
    Args:
        domain: Tech domain (e.g., 'python', 'data science', 'frontend')
        experience_level: Current level ('fresher', '1-3 years', '3-5 years', '5+ years')
    """
    roadmaps = {
        "python": {
            "fresher": {
                "month_1_3": ["Basics: syntax, loops, functions", "Data structures: lists, dicts, tuples", "OOP fundamentals"],
                "month_4_6": ["Popular libs: NumPy, Pandas, Requests", "Web scraping basics", "Build 2-3 small projects"],
                "month_7_12": ["Django/Flask frameworks", "Database (SQL/NoSQL)", "Deploy to production"],
            },
            "1-3 years": {
                "current": ["Advanced Python patterns", "FastAPI/async programming", "Testing & CI/CD"],
                "next_3_months": ["Microservices architecture", "Cloud (AWS/GCP)", "Leadership basics"],
            },
        },
        "data science": {
            "fresher": {
                "month_1_3": ["Statistics & Probability", "Python basics + NumPy/Pandas", "Data visualization (Matplotlib, Seaborn)"],
                "month_4_6": ["ML algorithms (Supervised, Unsupervised)", "scikit-learn & TensorFlow", "Build 2 ML projects"],
                "month_7_12": ["SQL for data analysis", "A/B testing & experimentation", "Kaggle competitions"],
            },
            "1-3 years": {
                "current": ["Advanced ML techniques", "Deep Learning (PyTorch, TensorFlow)", "Model deployment"],
                "next_3_months": ["MLOps & model monitoring", "Causal inference", "Leadership in data team"],
            },
        },
        "react": {
            "fresher": {
                "month_1_3": ["HTML/CSS/JavaScript fundamentals", "React basics: Components, Props, State", "Hooks: useState, useEffect"],
                "month_4_6": ["React Router for SPA", "State management (Redux/Context)", "API integration"],
                "month_7_12": ["TypeScript with React", "Performance optimization", "Build 3 production projects"],
            },
            "1-3 years": {
                "current": ["Advanced patterns: Custom hooks, Render props", "Testing (Jest, React Testing Library)", "Accessibility (a11y)"],
                "next_3_months": ["Next.js framework", "GraphQL", "Frontend architecture"],
            },
        },
        "devops": {
            "fresher": {
                "month_1_3": ["Linux fundamentals", "Docker containers", "Git & version control"],
                "month_4_6": ["Kubernetes basics", "CI/CD pipelines", "AWS services (EC2, S3, RDS)"],
                "month_7_12": ["Infrastructure as Code (Terraform)", "Monitoring & logging (ELK stack)", "Security best practices"],
            },
            "1-3 years": {
                "current": ["Advanced K8s patterns", "Cloud architecture", "Disaster recovery & HA"],
                "next_3_months": ["DevOps leadership", "FinOps (cost optimization)", "Service mesh (Istio)"],
            },
        },
    }
    
    domain_lower = domain.lower()
    roadmap = None
    
    for key in roadmaps:
        if key in domain_lower:
            roadmap = roadmaps[key]
            break
    
    if not roadmap:
        return f"🛣️ **Career Roadmap: {domain}**\n\nNo roadmap available. Try: Python, Data Science, React, or DevOps."
    
    result = f"🛣️ **Career Roadmap: {domain.title()} ({experience_level})**\n\n"
    
    path = roadmap.get(experience_level, roadmap.get("fresher", {}))
    
    for phase, items in path.items():
        result += f"### 📌 {phase.replace('_', ' ').title()}\n"
        result += "\n".join(f"  ✓ {item}" for item in items) + "\n\n"
    
    result += "**📚 Key Resources:**\n"
    result += "  • Udemy/Coursera courses\n"
    result += "  • Official documentation\n"
    result += "  • YouTube channels & blogs\n"
    result += "  • GitHub open-source projects\n"
    
    return result


def get_mock_interview_questions(role: str, round_num: int = 1) -> str:
    """
    Generate mock interview questions for practice.
    
    Args:
        role: Job role
        round_num: Interview round (1-Technical, 2-Manager, 3-HR)
    """
    questions = {
        "python": [
            "What's the difference between list and tuple?",
            "Explain Python's GIL and why it matters",
            "What are decorators and when do you use them?",
            "How does Python memory management work?",
            "Explain list comprehensions with an example",
            "What's the difference between *args and **kwargs?",
        ],
        "data scientist": [
            "Explain the bias-variance tradeoff",
            "How do you handle imbalanced datasets?",
            "Walk me through your approach to an ML problem",
            "What's the difference between precision and recall?",
            "How do you evaluate a regression model?",
            "Explain A/B testing and its importance",
        ],
        "react": [
            "Explain React hooks and when to use them",
            "What's virtual DOM and how does it work?",
            "Difference between useState and useReducer",
            "How do you optimize React performance?",
            "Explain controlled vs uncontrolled components",
            "What's the purpose of useCallback and useMemo?",
        ],
    }
    
    hr_questions = [
        "Tell me about yourself",
        "Why do you want to join our company?",
        "What are your strengths and weaknesses?",
        "Describe a challenging situation and how you handled it",
        "What's your long-term career goal?",
        "How do you handle teamwork and conflicts?",
    ]
    
    role_lower = role.lower()
    result = f"🎤 **Mock Interview Questions: {role}**\n\n"
    
    if round_num == 1:
        result += "### Technical Round\n\n"
        qs = None
        for key in questions:
            if key in role_lower:
                qs = questions[key]
                break
        qs = qs or questions["python"]
    elif round_num == 2:
        result += "### Manager Round\n\n"
        qs = ["How do you approach learning new technologies?", "Tell me about a project you're proud of", "How do you work in a team?"]
    else:
        result += "### HR Round\n\n"
        qs = hr_questions
    
    for i, q in enumerate(qs, 1):
        result += f"{i}. {q}\n"
    
    result += f"\n**💡 Tips:**\n"
    result += "  • Take 10-15 seconds to think before answering\n"
    result += "  • Use the STAR method for behavioral questions\n"
    result += "  • Ask clarifying questions\n"
    result += "  • Provide concrete examples\n"
    
    return result


def get_learning_recommendations(resume_gap: str = "", target_role: str = "") -> str:
    """
    Get personalized learning recommendations.
    
    Args:
        resume_gap: Skills gap to fill
        target_role: Target job role
    """
    recommendations = {
        "python": [
            {"type": "📚 Course", "item": "Complete Python Developer (Udemy) - ⭐ 4.8", "duration": "22 hours", "cost": "₹399"},
            {"type": "🎓 Certificate", "item": "Google Python Automation Certificate (Coursera) - ⭐ 4.7", "duration": "6 months", "cost": "Free + cert"},
            {"type": "🛠️ Project", "item": "Build a web scraper using BeautifulSoup", "duration": "2 weeks", "cost": "Free"},
            {"type": "🛠️ Project", "item": "Create a CLI automation tool", "duration": "2 weeks", "cost": "Free"},
        ],
        "data science": [
            {"type": "📚 Course", "item": "Andrew Ng's Machine Learning (Coursera) - ⭐ 4.9", "duration": "2 months", "cost": "Free + cert"},
            {"type": "🎓 Certificate", "item": "IBM Data Science Certificate (Coursera) - ⭐ 4.6", "duration": "5 months", "cost": "Free + cert"},
            {"type": "🛠️ Project", "item": "Kaggle house price prediction competition", "duration": "3 weeks", "cost": "Free"},
            {"type": "🛠️ Project", "item": "Customer segmentation using clustering", "duration": "2 weeks", "cost": "Free"},
        ],
        "react": [
            {"type": "📚 Course", "item": "The Complete React Course (Scrimba) - ⭐ 4.8", "duration": "20 hours", "cost": "₹5000"},
            {"type": "🎓 Certificate", "item": "React & Next.js Certification", "duration": "8 weeks", "cost": "₹10000"},
            {"type": "🛠️ Project", "item": "Build a full-stack e-commerce app", "duration": "4 weeks", "cost": "Free"},
            {"type": "🛠️ Project", "item": "Create a real-time chat application", "duration": "3 weeks", "cost": "Free"},
        ],
    }
    
    skill_lower = resume_gap.lower() if resume_gap else "python"
    
    result = f"📚 **Learning Recommendations: {skill_lower.title()}**\n\n"
    
    items = None
    for key in recommendations:
        if key in skill_lower:
            items = recommendations[key]
            break
    
    items = items or recommendations["python"]
    
    for item in items:
        result += f"**{item['type']}**: {item['item']}\n"
        result += f"   ⏱️ {item['duration']} | 💰 {item['cost']}\n\n"
    
    result += "**🎯 Learning Path Priority:**\n"
    result += "  1. Courses (Foundation)\n"
    result += "  2. Certifications (Credibility)\n"
    result += "  3. Projects (Portfolio)\n"
    
    return result


def get_personalized_recommendations(resume: str, interests: str = "", experience: str = "fresher") -> str:
    """
    Get personalized career and learning recommendations.
    
    Args:
        resume: User's resume content
        interests: User's interests
        experience: Years of experience
    """
    result = "🎯 **Personalized Recommendations Just For You**\n\n"
    
    if "fresher" in experience.lower() or "0" in experience:
        result += "### 🚀 For Freshers\n"
        result += "**Top Advice:**\n"
        result += "  1. **Network First**: Join tech communities, attend meetups\n"
        result += "  2. **Build Projects**: GitHub portfolio is your resume\n"
        result += "  3. **Intern First**: Gain 6 months-1 year experience\n"
        result += "  4. **Learn Continuously**: Pick one skill, master it\n"
        result += "  5. **Apply Smartly**: 100 applications > 1 perfect resume\n\n"
        result += "**Next Steps:**\n"
        result += "  ✓ Complete 2-3 projects in next 3 months\n"
        result += "  ✓ Get AWS/GCP certification\n"
        result += "  ✓ Apply to 50 companies (India + Remote)\n"
        result += "  ✓ Practice mock interviews\n\n"
    else:
        result += f"### 📈 For {experience.title()} Experience\n"
        result += "**Career Progression Path:**\n"
        result += "  • Lead projects and mentor juniors\n"
        result += "  • Move into technical leadership/management\n"
        result += "  • Specialize in emerging tech (AI/ML, Cloud)\n"
        result += "  • Build your personal brand\n\n"
    
    result += "**Best Companies for Your Profile:**\n"
    result += "  🔵 IT Services: TCS, Infosys, Wipro\n"
    result += "  🟢 Product Companies: Google, Amazon, Flipkart\n"
    result += "  🟡 Fast-growing Startups: Zepto, Meesho, PhonePe\n\n"
    
    result += "**Cities with Best Opportunities:**\n"
    result += "  1. Bangalore - 40% of all tech jobs\n"
    result += "  2. Hyderabad - Growing tech hub\n"
    result += "  3. Remote - Global opportunities\n\n"
    
    result += "**Action Items (Next 30 Days):**\n"
    result += "  ☐ Update resume with latest projects\n"
    result += "  ☐ Start one learning course\n"
    result += "  ☐ Practice 10 mock interviews\n"
    result += "  ☐ Apply to 20 target companies\n"
    result += "  ☐ Reach out to 5 connections on LinkedIn\n"
    
    return result