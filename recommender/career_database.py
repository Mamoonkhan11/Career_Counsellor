"""
Career Database and Recommendation Engine
Contains comprehensive career information and matching algorithms
"""

CAREER_DATABASE = {
    # Technology & Engineering
    "software_engineer": {
        "name": "Software Engineer",
        "domain": "Technology & Engineering",
        "description": "Design, develop, and maintain software applications",
        "key_interests": ["programming", "coding", "technology", "problem_solving", "logic"],
        "key_skills": ["python", "javascript", "java", "c++", "algorithms", "debugging"],
        "key_strengths": ["analytical_thinking", "attention_to_detail", "problem_solving"],
        "salary_range": "$80,000 - $150,000",
        "education": "Bachelor's in Computer Science or related field",
        "experience_level": "Entry to Senior",
        "work_environment": "Office, Remote, Hybrid",
        "growth_potential": "High",
        "job_satisfaction": "High",
        "work_life_balance": "Good",
        "future_outlook": "Excellent"
    },
    "data_scientist": {
        "name": "Data Scientist",
        "domain": "Technology & Engineering",
        "description": "Analyze complex data sets to help organizations make decisions",
        "key_interests": ["data", "statistics", "machine_learning", "analytics", "research"],
        "key_skills": ["python", "r", "sql", "machine_learning", "statistics", "data_visualization"],
        "key_strengths": ["analytical_thinking", "problem_solving", "mathematical_aptitude"],
        "salary_range": "$90,000 - $160,000",
        "education": "Master's in Data Science, Statistics, or related field",
        "experience_level": "Mid to Senior",
        "work_environment": "Office, Remote",
        "growth_potential": "Very High",
        "job_satisfaction": "High",
        "work_life_balance": "Good",
        "future_outlook": "Excellent"
    },
    "ai_engineer": {
        "name": "AI Engineer",
        "domain": "Technology & Engineering",
        "description": "Build and deploy artificial intelligence systems",
        "key_interests": ["ai", "machine_learning", "neural_networks", "automation"],
        "key_skills": ["python", "tensorflow", "pytorch", "deep_learning", "computer_vision"],
        "key_strengths": ["analytical_thinking", "innovation", "technical_expertise"],
        "salary_range": "$100,000 - $180,000",
        "education": "Master's in AI, Computer Science, or related field",
        "experience_level": "Mid to Senior",
        "work_environment": "Office, Research Lab, Remote",
        "growth_potential": "Very High",
        "job_satisfaction": "High",
        "work_life_balance": "Good",
        "future_outlook": "Excellent"
    },
    "cybersecurity_analyst": {
        "name": "Cybersecurity Analyst",
        "domain": "Technology & Engineering",
        "description": "Protect computer systems and networks from cyber threats",
        "key_interests": ["security", "networks", "hacking", "protection", "technology"],
        "key_skills": ["network_security", "ethical_hacking", "firewalls", "encryption"],
        "key_strengths": ["analytical_thinking", "attention_to_detail", "problem_solving"],
        "salary_range": "$85,000 - $140,000",
        "education": "Bachelor's in Cybersecurity or Computer Science",
        "experience_level": "Entry to Senior",
        "work_environment": "Office, Remote",
        "growth_potential": "High",
        "job_satisfaction": "High",
        "work_life_balance": "Good",
        "future_outlook": "Excellent"
    },
    "ux_ui_designer": {
        "name": "UX/UI Designer",
        "domain": "Arts & Design",
        "description": "Create intuitive and visually appealing user interfaces",
        "key_interests": ["design", "creativity", "user_experience", "visual_design"],
        "key_skills": ["figma", "sketch", "adobe_xd", "prototyping", "user_research"],
        "key_strengths": ["creativity", "attention_to_detail", "empathy", "communication"],
        "salary_range": "$70,000 - $130,000",
        "education": "Bachelor's in Design, HCI, or related field",
        "experience_level": "Entry to Senior",
        "work_environment": "Office, Freelance, Remote",
        "growth_potential": "High",
        "job_satisfaction": "High",
        "work_life_balance": "Good",
        "future_outlook": "Good"
    },
    "graphic_designer": {
        "name": "Graphic Designer",
        "domain": "Arts & Design",
        "description": "Create visual content for print and digital media",
        "key_interests": ["art", "creativity", "visual_design", "aesthetics"],
        "key_skills": ["photoshop", "illustrator", "indesign", "typography", "color_theory"],
        "key_strengths": ["creativity", "attention_to_detail", "artistic_ability"],
        "salary_range": "$50,000 - $90,000",
        "education": "Bachelor's in Graphic Design or Fine Arts",
        "experience_level": "Entry to Senior",
        "work_environment": "Office, Freelance, Agency",
        "growth_potential": "Medium",
        "job_satisfaction": "High",
        "work_life_balance": "Good",
        "future_outlook": "Stable"
    },
    "animator": {
        "name": "Animator",
        "domain": "Arts & Design",
        "description": "Create animated content for films, games, and media",
        "key_interests": ["animation", "storytelling", "visual_effects", "art"],
        "key_skills": ["maya", "blender", "after_effects", "storyboarding", "3d_modeling"],
        "key_strengths": ["creativity", "attention_to_detail", "visual_spatial_skills"],
        "salary_range": "$60,000 - $120,000",
        "education": "Bachelor's in Animation, Fine Arts, or related field",
        "experience_level": "Entry to Senior",
        "work_environment": "Studio, Remote, Freelance",
        "growth_potential": "Medium",
        "job_satisfaction": "High",
        "work_life_balance": "Variable",
        "future_outlook": "Good"
    },
    "architect": {
        "name": "Architect",
        "domain": "Arts & Design",
        "description": "Design buildings and structures with functionality and aesthetics",
        "key_interests": ["design", "construction", "aesthetics", "engineering"],
        "key_skills": ["autocad", "sketchup", "revit", "project_management", "building_codes"],
        "key_strengths": ["creativity", "spatial_reasoning", "attention_to_detail", "problem_solving"],
        "salary_range": "$70,000 - $130,000",
        "education": "Bachelor's in Architecture (5-year program)",
        "experience_level": "Entry to Senior",
        "work_environment": "Office, Site visits, Hybrid",
        "growth_potential": "Medium",
        "job_satisfaction": "High",
        "work_life_balance": "Good",
        "future_outlook": "Stable"
    },
    "business_analyst": {
        "name": "Business Analyst",
        "domain": "Business & Finance",
        "description": "Analyze business needs and recommend solutions",
        "key_interests": ["business", "analysis", "problem_solving", "strategy"],
        "key_skills": ["requirements_gathering", "data_analysis", "sql", "excel", "process_modeling"],
        "key_strengths": ["analytical_thinking", "communication", "problem_solving"],
        "salary_range": "$70,000 - $120,000",
        "education": "Bachelor's in Business, Information Systems, or related field",
        "experience_level": "Entry to Senior",
        "work_environment": "Office, Remote, Hybrid",
        "growth_potential": "High",
        "job_satisfaction": "High",
        "work_life_balance": "Good",
        "future_outlook": "Good"
    },
    "financial_analyst": {
        "name": "Financial Analyst",
        "domain": "Business & Finance",
        "description": "Analyze financial data to help organizations make investment decisions",
        "key_interests": ["finance", "investing", "markets", "economics", "numbers"],
        "key_skills": ["financial_modeling", "excel", "valuation", "risk_analysis", "accounting"],
        "key_strengths": ["analytical_thinking", "attention_to_detail", "mathematical_aptitude"],
        "salary_range": "$65,000 - $120,000",
        "education": "Bachelor's in Finance, Economics, or Business",
        "experience_level": "Entry to Senior",
        "work_environment": "Office, Remote",
        "growth_potential": "High",
        "job_satisfaction": "High",
        "work_life_balance": "Good",
        "future_outlook": "Good"
    },
    "marketing_manager": {
        "name": "Marketing Manager",
        "domain": "Business & Finance",
        "description": "Develop and execute marketing strategies for brands",
        "key_interests": ["marketing", "strategy", "creativity", "business", "communication"],
        "key_skills": ["digital_marketing", "seo", "content_strategy", "analytics", "brand_management"],
        "key_strengths": ["creativity", "communication", "strategic_thinking", "leadership"],
        "salary_range": "$75,000 - $140,000",
        "education": "Bachelor's in Marketing, Business, or Communications",
        "experience_level": "Mid to Senior",
        "work_environment": "Office, Remote, Hybrid",
        "growth_potential": "High",
        "job_satisfaction": "High",
        "work_life_balance": "Good",
        "future_outlook": "Good"
    },
    "physician": {
        "name": "Physician",
        "domain": "Healthcare & Science",
        "description": "Diagnose and treat patients with medical conditions",
        "key_interests": ["medicine", "healthcare", "helping_people", "science", "biology"],
        "key_skills": ["medical_knowledge", "diagnosis", "patient_care", "communication"],
        "key_strengths": ["empathy", "attention_to_detail", "stress_management", "ethical_judgment"],
        "salary_range": "$180,000 - $250,000",
        "education": "Doctor of Medicine (MD) - 4 years medical school + residency",
        "experience_level": "Senior",
        "work_environment": "Hospital, Clinic, Private Practice",
        "growth_potential": "High",
        "job_satisfaction": "High",
        "work_life_balance": "Variable",
        "future_outlook": "Good"
    },
    "nurse": {
        "name": "Registered Nurse",
        "domain": "Healthcare & Science",
        "description": "Provide patient care and support in healthcare settings",
        "key_interests": ["healthcare", "helping_people", "medicine", "compassion"],
        "key_skills": ["patient_care", "medical_procedures", "communication", "documentation"],
        "key_strengths": ["empathy", "attention_to_detail", "stress_management", "communication"],
        "salary_range": "$65,000 - $95,000",
        "education": "Associate or Bachelor's in Nursing + NCLEX-RN",
        "experience_level": "Entry to Senior",
        "work_environment": "Hospital, Clinic, Long-term care",
        "growth_potential": "Medium",
        "job_satisfaction": "High",
        "work_life_balance": "Variable",
        "future_outlook": "Good"
    },
    "research_scientist": {
        "name": "Research Scientist",
        "domain": "Healthcare & Science",
        "description": "Conduct scientific research to advance knowledge in various fields",
        "key_interests": ["research", "science", "discovery", "innovation", "analysis"],
        "key_skills": ["scientific_methods", "data_analysis", "lab_techniques", "publishing"],
        "key_strengths": ["analytical_thinking", "curiosity", "attention_to_detail", "persistence"],
        "salary_range": "$70,000 - $130,000",
        "education": "PhD in relevant scientific field",
        "experience_level": "Mid to Senior",
        "work_environment": "Laboratory, University, Research Institute",
        "growth_potential": "Medium",
        "job_satisfaction": "High",
        "work_life_balance": "Good",
        "future_outlook": "Good"
    },
    "lawyer": {
        "name": "Lawyer",
        "domain": "Law & Humanities",
        "description": "Provide legal advice and represent clients in legal matters",
        "key_interests": ["law", "justice", "debate", "research", "writing"],
        "key_skills": ["legal_research", "writing", "negotiation", "public_speaking", "analytical_thinking"],
        "key_strengths": ["analytical_thinking", "communication", "persuasion", "ethical_judgment"],
        "salary_range": "$80,000 - $180,000",
        "education": "Juris Doctor (JD) - 3 years law school",
        "experience_level": "Entry to Senior",
        "work_environment": "Law Firm, Corporate, Government",
        "growth_potential": "High",
        "job_satisfaction": "High",
        "work_life_balance": "Variable",
        "future_outlook": "Stable"
    },
    "journalist": {
        "name": "Journalist",
        "domain": "Law & Humanities",
        "description": "Research and report news and current events",
        "key_interests": ["writing", "research", "communication", "current_events", "storytelling"],
        "key_skills": ["writing", "interviewing", "research", "multimedia", "ethics"],
        "key_strengths": ["communication", "curiosity", "attention_to_detail", "objectivity"],
        "salary_range": "$40,000 - $100,000",
        "education": "Bachelor's in Journalism, Communications, or related field",
        "experience_level": "Entry to Senior",
        "work_environment": "Newsroom, Remote, Freelance",
        "growth_potential": "Medium",
        "job_satisfaction": "Medium",
        "work_life_balance": "Variable",
        "future_outlook": "Stable"
    },
    "teacher": {
        "name": "Teacher/Educator",
        "domain": "Law & Humanities",
        "description": "Educate and inspire students at various levels",
        "key_interests": ["teaching", "education", "helping_people", "knowledge_sharing"],
        "key_skills": ["teaching_methods", "communication", "curriculum_design", "assessment"],
        "key_strengths": ["communication", "patience", "organization", "inspiration"],
        "salary_range": "$45,000 - $85,000",
        "education": "Bachelor's in Education or subject area + teaching certification",
        "experience_level": "Entry to Senior",
        "work_environment": "School, University, Online",
        "growth_potential": "Medium",
        "job_satisfaction": "High",
        "work_life_balance": "Good",
        "future_outlook": "Stable"
    },
    "project_manager": {
        "name": "Project Manager",
        "domain": "Management & Leadership",
        "description": "Lead teams and manage projects to successful completion",
        "key_interests": ["leadership", "organization", "strategy", "teamwork"],
        "key_skills": ["project_planning", "team_leadership", "communication", "risk_management"],
        "key_strengths": ["leadership", "organization", "communication", "problem_solving"],
        "salary_range": "$80,000 - $140,000",
        "education": "Bachelor's in Business, Project Management, or related field + PMP certification",
        "experience_level": "Mid to Senior",
        "work_environment": "Office, Remote, Hybrid",
        "growth_potential": "High",
        "job_satisfaction": "High",
        "work_life_balance": "Good",
        "future_outlook": "Good"
    },
    "consultant": {
        "name": "Management Consultant",
        "domain": "Management & Leadership",
        "description": "Advise organizations on strategy, operations, and performance improvement",
        "key_interests": ["strategy", "business", "problem_solving", "analysis", "leadership"],
        "key_skills": ["strategic_planning", "data_analysis", "presentation", "change_management"],
        "key_strengths": ["analytical_thinking", "communication", "leadership", "adaptability"],
        "salary_range": "$90,000 - $160,000",
        "education": "MBA or Master's in Business, Consulting, or related field",
        "experience_level": "Mid to Senior",
        "work_environment": "Office, Client sites, Travel",
        "growth_potential": "High",
        "job_satisfaction": "High",
        "work_life_balance": "Variable",
        "future_outlook": "Good"
    },
    "hr_manager": {
        "name": "HR Manager",
        "domain": "Management & Leadership",
        "description": "Manage human resources functions including recruitment, development, and employee relations",
        "key_interests": ["people", "organization", "development", "leadership", "helping_people"],
        "key_skills": ["recruitment", "employee_development", "conflict_resolution", "hr_law"],
        "key_strengths": ["empathy", "communication", "leadership", "organizational_skills"],
        "salary_range": "$75,000 - $130,000",
        "education": "Bachelor's in HR, Business, Psychology + HR certifications",
        "experience_level": "Mid to Senior",
        "work_environment": "Office, Remote, Hybrid",
        "growth_potential": "Medium",
        "job_satisfaction": "High",
        "work_life_balance": "Good",
        "future_outlook": "Stable"
    }
}

# Abbreviation mappings
ABBREVIATION_MAP = {
    "it": ["information_technology", "tech", "technology"],
    "cs": ["computer_science", "coding", "programming"],
    "ai": ["artificial_intelligence", "machine_learning"],
    "ux": ["user_experience", "design"],
    "ui": ["user_interface", "design"],
    "ml": ["machine_learning", "data_science"],
    "ds": ["data_science", "analytics"],
    "dev": ["development", "programming"],
    "eng": ["engineering", "technical"],
    "biz": ["business", "management"],
    "fin": ["finance", "financial"],
    "mkt": ["marketing", "advertising"],
    "hr": ["human_resources", "people"],
    "pm": ["project_management", "leadership"],
    "ba": ["business_analysis", "analysis"],
    "qa": ["quality_assurance", "testing"],
    "se": ["software_engineer", "developer"],
    "fe": ["frontend", "web_development"],
    "be": ["backend", "server_side"],
    "fs": ["full_stack", "web_development"],
    # Technology-related terms
    "tech": ["technology", "computer", "software", "programming"],
    "technology": ["tech", "computer", "software", "programming", "it"],
    "computer": ["technology", "tech", "programming", "software"],
    "programming": ["coding", "software", "development", "tech"],
    "coding": ["programming", "software", "development", "tech"],
    "software": ["programming", "development", "tech", "technology"]
}

def normalize_interest(interest):
    """Normalize interests by expanding abbreviations and standardizing terms"""
    interest_lower = interest.lower().strip()

    # Check if it's an abbreviation
    if interest_lower in ABBREVIATION_MAP:
        return ABBREVIATION_MAP[interest_lower]

    # Return as list for consistency
    return [interest_lower]

def get_career_by_id(career_id):
    """Get career details by ID"""
    return CAREER_DATABASE.get(career_id)

def get_all_careers():
    """Get all careers in the database"""
    return CAREER_DATABASE

def get_careers_by_domain(domain):
    """Get careers filtered by domain"""
    return {k: v for k, v in CAREER_DATABASE.items() if v["domain"] == domain}

def search_careers_by_keywords(keywords):
    """Search careers by keywords in interests, skills, or strengths"""
    matching_careers = {}

    for career_id, career_data in CAREER_DATABASE.items():
        score = 0
        matched_keywords = []

        for keyword in keywords:
            keyword_lower = keyword.lower()

            # Check interests
            if any(keyword_lower in interest for interest in career_data["key_interests"]):
                score += 3
                matched_keywords.append(f"interest: {keyword}")

            # Check skills
            if any(keyword_lower in skill for skill in career_data["key_skills"]):
                score += 2
                matched_keywords.append(f"skill: {keyword}")

            # Check strengths
            if any(keyword_lower in strength for strength in career_data["key_strengths"]):
                score += 2
                matched_keywords.append(f"strength: {keyword}")

            # Check name and description
            if keyword_lower in career_data["name"].lower() or keyword_lower in career_data["description"].lower():
                score += 1
                matched_keywords.append(f"description: {keyword}")

        if score > 0:
            matching_careers[career_id] = {
                "career": career_data,
                "score": score,
                "matched_keywords": matched_keywords
            }

    # Sort by score descending
    return dict(sorted(matching_careers.items(), key=lambda x: x[1]["score"], reverse=True))
