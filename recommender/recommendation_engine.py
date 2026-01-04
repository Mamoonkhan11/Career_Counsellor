"""
Career Recommendation Engine
Implements intelligent matching algorithms for career recommendations
"""

import math
from .career_database import CAREER_DATABASE, normalize_interest, search_careers_by_keywords

class CareerRecommender:
    def __init__(self):
        self.career_db = CAREER_DATABASE

    def calculate_match_score(self, user_profile, career_data):
        """
        Calculate how well a career matches a user's profile
        Returns score between 0-100 and explanation
        """
        score = 0
        max_score = 100
        explanations = []

        # Interest matching (40% weight)
        interest_score = self._calculate_interest_score(user_profile.get('interests', []), career_data)
        score += interest_score * 0.4
        if interest_score > 0:
            explanations.append(f"Interest alignment: {interest_score}%")

        # Skills matching (30% weight)
        skills_score = self._calculate_skills_score(user_profile.get('skills', []), career_data)
        score += skills_score * 0.3
        if skills_score > 0:
            explanations.append(f"Skills match: {skills_score}%")

        # Strengths matching (20% weight)
        strengths_score = self._calculate_strengths_score(user_profile.get('strengths', []), career_data)
        score += strengths_score * 0.2
        if strengths_score > 0:
            explanations.append(f"Strengths alignment: {strengths_score}%")

        # Preferences bonus (10% weight)
        preferences_score = self._calculate_preferences_score(user_profile.get('preferences', []), career_data)
        score += preferences_score * 0.1
        if preferences_score > 0:
            explanations.append(f"Preferences match: {preferences_score}%")

        return min(round(score), 100), explanations

    def _calculate_interest_score(self, user_interests, career_data):
        """Calculate interest matching score"""
        if not user_interests:
            return 0

        total_score = 0
        matched_interests = []

        for user_interest in user_interests:
            # Normalize the interest (handle abbreviations)
            normalized_interests = normalize_interest(user_interest)

            for norm_interest in normalized_interests:
                # Check exact matches
                if norm_interest in career_data["key_interests"]:
                    total_score += 100
                    matched_interests.append(norm_interest)
                # Check partial matches
                elif any(norm_interest in interest for interest in career_data["key_interests"]):
                    total_score += 60
                    matched_interests.append(norm_interest)
                # Check related concepts
                elif self._are_related_concepts(norm_interest, career_data["key_interests"]):
                    total_score += 30
                    matched_interests.append(norm_interest)

        # Average score across all interests, but cap at 100
        if user_interests:
            avg_score = total_score / len(user_interests)
            return min(avg_score, 100)
        return 0

    def _calculate_skills_score(self, user_skills, career_data):
        """Calculate skills matching score"""
        if not user_skills:
            return 0

        matched_skills = 0
        for skill in user_skills:
            skill_lower = skill.lower()
            if any(skill_lower in career_skill for career_skill in career_data["key_skills"]):
                matched_skills += 1

        return (matched_skills / len(user_skills)) * 100 if user_skills else 0

    def _calculate_strengths_score(self, user_strengths, career_data):
        """Calculate strengths matching score"""
        if not user_strengths:
            return 0

        matched_strengths = 0
        for strength in user_strengths:
            strength_lower = strength.lower()
            if any(strength_lower in career_strength for career_strength in career_data["key_strengths"]):
                matched_strengths += 1

        return (matched_strengths / len(user_strengths)) * 100 if user_strengths else 0

    def _calculate_preferences_score(self, user_preferences, career_data):
        """Calculate preferences matching score"""
        if not user_preferences:
            return 0

        # Simple preference matching - can be expanded
        preference_keywords = {
            "remote": ["remote", "flexible", "work_from_home"],
            "travel": ["travel", "business_trip"],
            "creative": ["creativity", "innovation"],
            "leadership": ["leadership", "management"],
            "teamwork": ["team", "collaboration"],
            "independent": ["independent", "autonomous"]
        }

        matched_prefs = 0
        for pref in user_preferences:
            pref_lower = pref.lower()
            for pref_category, keywords in preference_keywords.items():
                if any(keyword in pref_lower for keyword in keywords):
                    # Check if career supports this preference
                    work_env = career_data.get("work_environment", "").lower()
                    if pref_category in work_env or any(keyword in work_env for keyword in keywords):
                        matched_prefs += 1
                        break

        return (matched_prefs / len(user_preferences)) * 100 if user_preferences else 0

    def _are_related_concepts(self, concept, career_interests):
        """Check if a concept is related to career interests using semantic similarity"""
        # Simple semantic relationships - can be enhanced with word embeddings
        related_terms = {
            "tech": ["technology", "computer", "software", "programming", "it"],
            "technology": ["tech", "computer", "software", "programming", "it", "coding"],
            "computer": ["technology", "programming", "software", "tech", "it"],
            "programming": ["coding", "software", "development", "tech", "technology"],
            "coding": ["programming", "software", "development", "tech", "technology"],
            "software": ["programming", "development", "tech", "technology", "computer"],
            "it": ["information_technology", "tech", "technology", "computer", "software"],
            "data": ["analytics", "statistics", "information", "database"],
            "creative": ["art", "design", "innovation", "creativity"],
            "business": ["management", "finance", "strategy", "entrepreneurship"],
            "science": ["research", "analysis", "discovery", "laboratory"],
            "people": ["social", "communication", "helping", "human"],
            "numbers": ["mathematics", "analytics", "finance", "statistics"],
            "logic": ["analytical", "problem_solving", "reasoning", "algorithm"]
        }

        concept_lower = concept.lower()
        if concept_lower in related_terms:
            return any(term in career_interests for term in related_terms[concept_lower])

        # Check reverse relationships
        for related_list in related_terms.values():
            if concept_lower in related_list:
                return any(term in career_interests for term in related_terms.keys()
                          if concept_lower in related_terms.get(term, []))

        return False

    def recommend_careers(self, user_profile, top_n=5):
        """
        Recommend top N careers based on user profile
        Returns list of career recommendations with scores and explanations
        """
        recommendations = []

        for career_id, career_data in self.career_db.items():
            score, explanations = self.calculate_match_score(user_profile, career_data)

            if score > 20:  # Minimum threshold for recommendations
                recommendations.append({
                    "career_id": career_id,
                    "career_name": career_data["name"],
                    "domain": career_data["domain"],
                    "description": career_data["description"],
                    "match_score": score,
                    "confidence": self._calculate_confidence(score),
                    "explanations": explanations,
                    "key_requirements": career_data["key_skills"][:3],  # Top 3 skills
                    "salary_range": career_data["salary_range"],
                    "education": career_data["education"],
                    "why_it_fits": self._generate_fit_explanation(user_profile, career_data, explanations)
                })

        # Sort by score descending and return top N
        recommendations.sort(key=lambda x: x["match_score"], reverse=True)
        return recommendations[:top_n]

    def _calculate_confidence(self, score):
        """Convert match score to confidence level"""
        if score >= 80:
            return "High"
        elif score >= 60:
            return "Medium-High"
        elif score >= 40:
            return "Medium"
        elif score >= 20:
            return "Low-Medium"
        else:
            return "Low"

    def _generate_fit_explanation(self, user_profile, career_data, explanations):
        """Generate a human-readable explanation of why this career fits"""
        reasons = []

        # Interest-based reasons
        user_interests = user_profile.get('interests', [])
        career_interests = career_data["key_interests"]
        matching_interests = [interest for interest in user_interests
                            if any(normalize_interest(interest)[0] in career_interests
                                  for interest in normalize_interest(interest))]

        if matching_interests:
            reasons.append(f"Aligns with your interests in {', '.join(matching_interests[:2])}")

        # Skills-based reasons
        user_skills = user_profile.get('skills', [])
        career_skills = career_data["key_skills"]
        matching_skills = [skill for skill in user_skills
                          if any(skill.lower() in career_skill for career_skill in career_skills)]

        if matching_skills:
            reasons.append(f"Leverages your skills in {', '.join(matching_skills[:2])}")

        # Strengths-based reasons
        user_strengths = user_profile.get('strengths', [])
        career_strengths = career_data["key_strengths"]
        matching_strengths = [strength for strength in user_strengths
                             if any(strength.lower() in career_strength for career_strength in career_strengths)]

        if matching_strengths:
            reasons.append(f"Matches your strengths in {', '.join(matching_strengths[:2])}")

        # Domain reason
        reasons.append(f"Falls within the {career_data['domain']} domain")

        return " • ".join(reasons)

    def get_career_details(self, career_id):
        """Get detailed information about a specific career"""
        career_data = self.career_db.get(career_id)
        if not career_data:
            return None

        return {
            "name": career_data["name"],
            "description": career_data["description"],
            "domain": career_data["domain"],
            "key_skills": career_data["key_skills"],
            "key_interests": career_data["key_interests"],
            "key_strengths": career_data["key_strengths"],
            "salary_range": career_data["salary_range"],
            "education": career_data["education"],
            "experience_level": career_data["experience_level"],
            "work_environment": career_data["work_environment"],
            "growth_potential": career_data["growth_potential"],
            "work_life_balance": career_data["work_life_balance"],
            "future_outlook": career_data["future_outlook"]
        }

    def generate_learning_plan(self, career_id):
        """Generate a learning plan for a specific career"""
        career_data = self.career_db.get(career_id)
        if not career_data:
            return None

        # Create a basic learning roadmap
        base_learning_plan = {
            "career": career_data["name"],
            "duration_months": 6,
            "phases": [
                {
                    "phase": "Foundation",
                    "duration": "2 months",
                    "focus": "Build core knowledge",
                    "resources": [
                        "Online courses on Coursera/Udemy",
                        "FreeCodeCamp or Khan Academy",
                        "Official documentation"
                    ]
                },
                {
                    "phase": "Skills Development",
                    "duration": "3 months",
                    "focus": "Develop practical skills",
                    "resources": [
                        "Hands-on projects",
                        "Personal portfolio",
                        "Open source contributions"
                    ]
                },
                {
                    "phase": "Specialization",
                    "duration": "1 month",
                    "focus": "Deepen expertise",
                    "resources": [
                        "Advanced courses",
                        "Certifications",
                        "Industry conferences"
                    ]
                }
            ],
            "key_skills_to_learn": career_data["key_skills"][:5],
            "recommended_certifications": self._get_certifications_for_career(career_id),
            "career_progression": self._get_career_progression(career_id)
        }

        return base_learning_plan

    def _get_certifications_for_career(self, career_id):
        """Get recommended certifications for a career"""
        certification_map = {
            "software_engineer": ["AWS Certified Developer", "Google Cloud Professional", "Microsoft Azure Fundamentals"],
            "data_scientist": ["IBM Data Science Professional Certificate", "Google Data Analytics", "TensorFlow Developer Certificate"],
            "ai_engineer": ["AWS Machine Learning Specialty", "Google Cloud AI/ML", "Deep Learning Specialization"],
            "cybersecurity_analyst": ["CompTIA Security+", "CISSP", "CEH (Certified Ethical Hacker)"],
            "ux_ui_designer": ["Google UX Design", "Adobe Certified Expert", "Interaction Design Foundation"],
            "business_analyst": ["CBAP (Certified Business Analysis Professional)", "PMI-PBA", "ECBA"],
            "financial_analyst": ["CFA (Chartered Financial Analyst)", "FRM", "CPA"],
            "project_manager": ["PMP (Project Management Professional)", "CSM (Certified ScrumMaster)", "PRINCE2"]
        }

        return certification_map.get(career_id, ["Industry-specific certifications"])

    def _get_career_progression(self, career_id):
        """Get career progression path"""
        progression_map = {
            "software_engineer": ["Junior Developer", "Mid-level Developer", "Senior Developer", "Tech Lead", "Engineering Manager"],
            "data_scientist": ["Data Analyst", "Junior Data Scientist", "Data Scientist", "Senior Data Scientist", "Data Science Manager"],
            "ux_ui_designer": ["Junior Designer", "UX/UI Designer", "Senior Designer", "Design Lead", "Design Manager"],
            "business_analyst": ["Business Analyst", "Senior Business Analyst", "Business Analysis Manager", "IT Business Partner"],
            "project_manager": ["Associate PM", "Project Manager", "Senior PM", "Program Manager", "PMO Director"]
        }

        return progression_map.get(career_id, ["Entry Level", "Mid Level", "Senior Level", "Management", "Executive"])
