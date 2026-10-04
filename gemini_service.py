import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def process_interests(user_interests):

    # Try Gemini first
    try:
        prompt = f"""
You are an AI assistant for a YouTube discovery application.

The user is interested in:
{user_interests}

Convert these interests into 5 useful YouTube search topics.

Return ONLY one topic per line.
No numbering.
No explanations.
"""

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        topics = response.text.strip().split("\n")

        topics = [
            topic.strip()
            for topic in topics
            if topic.strip()
        ]

        if topics:
            return topics[:5]

    except Exception:
        pass


    # Fallback if Gemini is temporarily unavailable
    interests = [
        interest.strip()
        for interest in user_interests.split(",")
        if interest.strip()
    ]

    topics = []

    for interest in interests:
        topics.append(f"{interest} tutorials")
        topics.append(f"{interest} projects")

    return topics[:5]