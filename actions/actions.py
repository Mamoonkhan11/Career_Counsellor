"""
Custom Actions for Career Counselling Bot
Handles entity extraction, career recommendations, and conversation flow
"""

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.forms import FormAction

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from recommender.recommendation_engine import CareerRecommender
from recommender.career_database import normalize_interest

class ActionExtractEntities(Action):
    """Extract and normalize entities from user input"""

    def name(self) -> Text:
        return "action_extract_entities"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get entities from the latest message
        entities = tracker.latest_message.get('entities', [])

        # Extract different entity types
        interests = []
        skills = []
        strengths = []
        preferences = []

        for entity in entities:
            entity_type = entity.get('entity')
            entity_value = entity.get('value')

            if entity_type == 'interest':
                # Normalize interests (handle abbreviations)
                normalized = normalize_interest(entity_value)
                interests.extend(normalized)
            elif entity_type == 'skill':
                skills.append(entity_value.lower())
            elif entity_type == 'strength':
                strengths.append(entity_value.lower())
            elif entity_type == 'preference':
                preferences.append(entity_value.lower())

        # Update slots with current values (merge with existing)
        current_interests = tracker.get_slot('interests') or []
        current_skills = tracker.get_slot('skills') or []
        current_strengths = tracker.get_slot('strengths') or []
        current_preferences = tracker.get_slot('preferences') or []

        # Merge new entities with existing ones
        all_interests = list(set(current_interests + interests))
        all_skills = list(set(current_skills + skills))
        all_strengths = list(set(current_strengths + strengths))
        all_preferences = list(set(current_preferences + preferences))

        return [
            SlotSet("interests", all_interests),
            SlotSet("skills", all_skills),
            SlotSet("strengths", all_strengths),
            SlotSet("preferences", all_preferences)
        ]

class ActionRecommendCareers(Action):
    """Recommend careers based on user's profile"""

    def name(self) -> Text:
        return "action_recommend_careers"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get user profile from slots
        interests = tracker.get_slot('interests') or []
        skills = tracker.get_slot('skills') or []
        strengths = tracker.get_slot('strengths') or []
        preferences = tracker.get_slot('preferences') or []

        # Check if we have enough information
        if not interests and not skills and not strengths:
            dispatcher.utter_message(text="I'd love to give you personalized career recommendations, but I need to know more about your interests, skills, or strengths. Could you tell me what you're passionate about or what you're good at?")
            return []

        # Create user profile
        user_profile = {
            'interests': interests,
            'skills': skills,
            'strengths': strengths,
            'preferences': preferences
        }

        # Get recommendations
        recommender = CareerRecommender()
        recommendations = recommender.recommend_careers(user_profile, top_n=5)

        if not recommendations:
            dispatcher.utter_message(text="I couldn't find strong matches with the information you provided. Could you tell me more about your interests or skills? Sometimes using different words can help me understand better.")
            return []

        # Format recommendations for display
        response_parts = []
        response_parts.append("🎯 Based on what you've shared, here are career paths that align well with your profile:")

        for i, rec in enumerate(recommendations[:3], 1):  # Top 3 recommendations
            emoji_map = {1: "🥇", 2: "🥈", 3: "🥉"}
            emoji = emoji_map.get(i, "⭐")

            response_parts.append(f"\n{emoji} **{rec['career_name']}**")
            response_parts.append(f"   💼 *{rec['domain']}*")
            response_parts.append(f"   📊 *Match Score: {rec['match_score']}% ({rec['confidence']} confidence)*")
            response_parts.append(f"   💰 *Salary Range: {rec['salary_range']}*")
            response_parts.append(f"   ✅ *Why it fits:* {rec['why_it_fits']}")

            # Show key requirements
            if rec['key_requirements']:
                reqs = ", ".join(rec['key_requirements'][:3])
                response_parts.append(f"   🛠️ *Key Skills:* {reqs}")

        response_parts.append("\n🤔 Would you like me to elaborate on any of these careers, or explore different options based on specific preferences?")

        full_response = "\n".join(response_parts)
        dispatcher.utter_message(text=full_response)

        # Store recommendations in slot for later reference
        career_list = [rec['career_id'] for rec in recommendations]
        return [SlotSet("current_career_recommendations", career_list)]

class ActionProvideCareerDetails(Action):
    """Provide detailed information about a specific career"""

    def name(self) -> Text:
        return "action_provide_career_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get the career from entities or context
        entities = tracker.latest_message.get('entities', [])
        career_entity = None

        for entity in entities:
            if entity.get('entity') == 'career':
                career_entity = entity.get('value')
                break

        # If no career entity found, check current recommendations
        if not career_entity:
            current_recs = tracker.get_slot('current_career_recommendations') or []
            if current_recs:
                # For now, provide details about the first recommendation
                career_entity = current_recs[0]

        if not career_entity:
            dispatcher.utter_message(text="I'd be happy to provide more details about a specific career. Which career from the recommendations interests you most?")
            return []

        # Get career details
        recommender = CareerRecommender()
        career_details = recommender.get_career_details(career_entity)

        if not career_details:
            dispatcher.utter_message(text="I couldn't find details for that career. Could you be more specific about which career you'd like to learn about?")
            return []

        # Format detailed response
        response_parts = []
        response_parts.append(f"📋 **Detailed Information: {career_details['name']}**")
        response_parts.append(f"📖 *Description:* {career_details['description']}")
        response_parts.append(f"🏢 *Domain:* {career_details['domain']}")

        response_parts.append("\n🛠️ **Key Skills Required:**")
        for skill in career_details['key_skills']:
            response_parts.append(f"   • {skill}")

        response_parts.append("\n💼 **Key Interests:**")
        for interest in career_details['key_interests']:
            response_parts.append(f"   • {interest}")

        response_parts.append("\n💪 **Key Strengths:**")
        for strength in career_details['key_strengths']:
            response_parts.append(f"   • {strength}")

        response_parts.append("\n📊 **Career Details:**")
        response_parts.append(f"   🎓 *Education:* {career_details['education']}")
        response_parts.append(f"   💰 *Salary Range:* {career_details['salary_range']}")
        response_parts.append(f"   📈 *Growth Potential:* {career_details['growth_potential']}")
        response_parts.append(f"   ⚖️ *Work-Life Balance:* {career_details['work_life_balance']}")
        response_parts.append(f"   🔮 *Future Outlook:* {career_details['future_outlook']}")
        response_parts.append(f"   🏢 *Work Environment:* {career_details['work_environment']}")

        full_response = "\n".join(response_parts)
        dispatcher.utter_message(text=full_response)

        return []

class ActionGenerateLearningPlan(Action):
    """Generate a learning plan for a selected career"""

    def name(self) -> Text:
        return "action_generate_learning_plan"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get the career from entities or current recommendations
        entities = tracker.latest_message.get('entities', [])
        career_entity = None

        for entity in entities:
            if entity.get('entity') == 'career':
                career_entity = entity.get('value')
                break

        # If no career entity found, check current recommendations
        if not career_entity:
            current_recs = tracker.get_slot('current_career_recommendations') or []
            if current_recs:
                career_entity = current_recs[0]

        if not career_entity:
            dispatcher.utter_message(text="To create a learning plan, I need to know which career you're interested in. Which career from the recommendations appeals to you most?")
            return []

        # Generate learning plan
        recommender = CareerRecommender()
        learning_plan = recommender.generate_learning_plan(career_entity)

        if not learning_plan:
            dispatcher.utter_message(text="I couldn't generate a learning plan for that career. Let me know if you'd like recommendations for a different career.")
            return []

        # Format learning plan response
        response_parts = []
        response_parts.append(f"📚 **Learning Plan for {learning_plan['career']}**")
        response_parts.append(f"⏱️ *Estimated Duration: {learning_plan['duration_months']} months*")

        for phase in learning_plan['phases']:
            response_parts.append(f"\n📌 **{phase['phase']} Phase** ({phase['duration']})")
            response_parts.append(f"   🎯 *Focus:* {phase['focus']}")
            response_parts.append("   📖 *Resources:*")
            for resource in phase['resources']:
                response_parts.append(f"      • {resource}")

        response_parts.append("\n🛠️ **Key Skills to Learn:**")
        for skill in learning_plan['key_skills_to_learn']:
            response_parts.append(f"   • {skill}")

        response_parts.append("\n🏆 **Recommended Certifications:**")
        for cert in learning_plan['recommended_certifications']:
            response_parts.append(f"   • {cert}")

        response_parts.append("\n📈 **Career Progression Path:**")
        progression = " → ".join(learning_plan['career_progression'])
        response_parts.append(f"   {progression}")

        response_parts.append("\n💡 *Pro tip:* Start with free resources, build a portfolio, and network with professionals in the field!")

        full_response = "\n".join(response_parts)
        dispatcher.utter_message(text=full_response)

        return []

class ActionExportCareerPlan(Action):
    """Export career plan as PDF (placeholder for now)"""

    def name(self) -> Text:
        return "action_export_career_plan"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get user profile and recommendations
        interests = tracker.get_slot('interests') or []
        skills = tracker.get_slot('skills') or []
        strengths = tracker.get_slot('strengths') or []
        recommendations = tracker.get_slot('current_career_recommendations') or []

        if not recommendations:
            dispatcher.utter_message(text="I don't have any career recommendations to export yet. Let's start by exploring your interests and getting some personalized recommendations first!")
            return []

        # For now, provide a summary that could be exported
        response_parts = []
        response_parts.append("📄 **Career Exploration Summary**")
        response_parts.append("\n👤 **Your Profile:**")
        if interests:
            response_parts.append(f"   💡 *Interests:* {', '.join(interests)}")
        if skills:
            response_parts.append(f"   🛠️ *Skills:* {', '.join(skills)}")
        if strengths:
            response_parts.append(f"   💪 *Strengths:* {', '.join(strengths)}")

        response_parts.append("\n🎯 **Recommended Careers:**")
        recommender = CareerRecommender()
        for career_id in recommendations[:3]:
            career_details = recommender.get_career_details(career_id)
            if career_details:
                response_parts.append(f"   • {career_details['name']} ({career_details['domain']})")

        response_parts.append("\n💾 *In a full implementation, this would be exported as a PDF with detailed recommendations, learning plans, and next steps.*")
        response_parts.append("\n📧 *For now, you can save this summary or take a screenshot for your records!*")

        full_response = "\n".join(response_parts)
        dispatcher.utter_message(text=full_response)

        return []
