import json

from google.api_core.exceptions import ResourceExhausted

from src.ai.groq_client import (
    GroqClient
)


class AIStoryGenerator:

    def __init__(self):

        self.client = GroqClient()

    def generate(
        self,
        caption: str
    ):

        prompt = f"""
You are an AI-powered Instagram Trend Detection Engine.

Return ONLY valid JSON.

Schema:

{{
  "trend_candidate": true,
  "category": "",
  "story": "",
  "summary": "",
  "entities": [],
  "keywords": [],
  "confidence": 0.95
}}

Ignore:

- engagement bait
- birth month posts
- quizzes
- memes
- horoscope
- comment bait
- tag your friend

Caption:

{caption}
"""

        try:

            response = self.client.generate(
                prompt
            )

            start = response.find("{")

            end = response.rfind("}") + 1

            return json.loads(
                response[start:end]
            )

        except ResourceExhausted:

            print(
                "\nGemini quota exceeded."
            )

            return None

        except Exception as e:

            print(
                f"\nGemini Error: {e}"
            )

            return None