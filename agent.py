from groq import Groq
from tools.job_tools import (
    search_jobs_tool,
    get_salary_info_tool,
    get_company_info_tool,
    get_interview_tips_tool,
    get_career_roadmap,
    get_indian_job_market_tool,
)

SYSTEM_PROMPT = """You are an expert Indian Job Market Career Assistant.
You help with:
1. Finding jobs in India with specific companies, salaries in LPA, locations
2. Salary benchmarks in LPA format
3. Company research (TCS, Infosys, Flipkart, Google India etc.)
4. Interview preparation and tips
5. Resume optimization for ATS systems
6. Career guidance for Indian job market

Always give salaries in LPA, mention Indian cities, be specific and use emojis."""


class JobSearchAgent:
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)

    def chat(self, user_message: str, history: list) -> str:
        try:
            msg_lower = user_message.lower()
            
            # Common role/city/experience lists for extraction
            ROLES = ["python", "java", "react", "devops", "data scientist", "data analyst", "frontend", "backend", "full stack", "ml engineer"]
            ROADMAP_DOMAINS = ["python developer", "data scientist", "react developer", "devops engineer", "java developer"]
            CITIES = ["bangalore", "mumbai", "hyderabad", "pune", "delhi", "chennai", "remote", "noida", "gurgaon"]
            tool_result = ""

            if any(word in msg_lower for word in ["find", "job", "hiring", "vacancy", "fresher", "opening", "developer", "engineer"]):
                role = "Software Engineer"
                location = "Bangalore"
                experience = "Fresher"
                for r in ROLES:
                    if r in msg_lower:
                        role = r
                        break
                for city in CITIES:
                    if city in msg_lower:
                        location = city.capitalize()
                        break
                if "fresher" in msg_lower:
                    experience = "Fresher"
                elif any(x in msg_lower for x in ["1-3", "1 year", "2 year"]):
                    experience = "1-3 years"
                elif any(x in msg_lower for x in ["3-5", "4 year", "5 year"]):
                    experience = "3-5 years"
                elif "senior" in msg_lower or "5+" in msg_lower:
                    experience = "5+ years"
                tool_result = search_jobs_tool(role, location, experience)

            elif any(word in msg_lower for word in ["salary", "lpa", "pay", "ctc", "package", "compensation"]):
                role = "Software Engineer"
                for r in ROLES:
                    if r in msg_lower:
                        role = r
                        break
                experience = "fresher"
                if any(x in msg_lower for x in ["1", "2", "3 year"]):
                    experience = "1-3 years"
                elif any(x in msg_lower for x in ["4", "5 year"]):
                    experience = "3-5 years"
                elif "senior" in msg_lower:
                    experience = "5+"
                tool_result = get_salary_info_tool(role, experience)

            elif any(word in msg_lower for word in ["tcs", "infosys", "wipro", "flipkart", "amazon", "google", "company", "culture", "review"]):
                company = "tcs"
                for c in ["tcs", "infosys", "wipro", "flipkart", "amazon", "google", "zomato"]:
                    if c in msg_lower:
                        company = c
                        break
                tool_result = get_company_info_tool(company)

            elif any(word in msg_lower for word in ["interview", "question", "prepare", "tips", "crack"]):
                role = "Software Engineer"
                for r in ["python", "java", "react", "devops", "data scientist"]:
                    if r in msg_lower:
                        role = r
                        break
                tool_result = get_interview_tips_tool(role)

            elif any(word in msg_lower for word in ["skill", "trend", "market", "demand", "hot"]):
                tool_result = get_indian_job_market_tool("IT")

            elif any(word in msg_lower for word in ["roadmap", "career path", "learning plan", "skill path", "growth plan"]):
                domain = "Python Developer" # Default
                experience = "fresher" # Default

                # Extract domain
                for d_role in ROADMAP_DOMAINS:
                    if d_role in msg_lower:
                        domain = d_role.title()
                        break
                
                # Extract experience
                if "fresher" in msg_lower:
                    experience = "fresher"
                elif any(x in msg_lower for x in ["1-3 years", "1 year", "2 year", "3 year"]):
                    experience = "1-3 years"
                elif any(x in msg_lower for x in ["3-5 years", "4 year", "5 year"]):
                    experience = "3-5 years"
                elif any(x in msg_lower for x in ["senior", "5+ years", "6 year", "7 year", "8 year", "9 year", "10+ year"]):
                    experience = "5+ years"
                
                tool_result = get_career_roadmap(domain, experience)

            if tool_result:
                prompt = "User asked: " + user_message + "\n\nData found:\n" + tool_result + "\n\nGive a helpful, well formatted response using this data. Add your own insights and advice. Use emojis."
            else:
                prompt = user_message

            # Construct conversation history including the new prompt
            messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history + [{"role": "user", "content": prompt}]

            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages,
                max_tokens=2048,
            )
            return response.choices[0].message.content

        except Exception as e:
            return "Error: " + str(e)