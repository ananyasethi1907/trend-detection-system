import json

from src.ai.groq_client import GroqClient


class LLMCanonicalResolver:

    _client = None

    @classmethod
    def _get_client(cls):
        if cls._client is None:
            cls._client = GroqClient()
        return cls._client

    @staticmethod
    def _build_prompt(caption, candidates):

        existing_topics = (
            "\n".join(f"- {topic}" for topic in candidates)
            if candidates else
            "None"
        )

        return f"""
You are an expert trend analyst for Instagram.

Your job is to understand the REAL STORY behind an Instagram caption.

DO NOT summarize.

DO NOT extract keywords.

DO NOT return a person's name.

Instead identify the actual event, discussion, controversy,
announcement, launch, debate, relationship update,
sports moment, meme or viral trend.

--------------------------------------------------
EXISTING TOPICS
--------------------------------------------------

{existing_topics}

Reuse an existing topic ONLY if it clearly matches.

Otherwise create ONE better headline.

--------------------------------------------------
GOOD OUTPUTS
--------------------------------------------------

Caption:
Matt Damon reveals the one rule that saved his marriage.

Headline:
Matt Damon Reveals Marriage Rule

Caption:
Jennifer Garner praises Ben Affleck as a father.

Headline:
Jennifer Garner Praises Ben Affleck

Caption:
Tom Holland and Zendaya spotted together at Wimbledon.

Headline:
Tom Holland and Zendaya at Wimbledon

Caption:
Coldplay performs before 1 lakh fans in Ahmedabad.

Headline:
Coldplay Ahmedabad Concert

Caption:
Meta launches AI editing tools.

Headline:
Meta Launches AI Editing Tools

Caption:
People debate whether smoking is a dealbreaker in dating.

Headline:
Dating Preferences Debate

Caption:
Everyone is buying Labubu dolls.

Headline:
Labubu Collectible Trend

Caption:
Logan Paul attends Palm Tree Crew event.

Headline:
Logan Paul Attends Palm Tree Crew Event

--------------------------------------------------
BAD OUTPUTS
--------------------------------------------------

Matt Damon
Jennifer Garner
Marriage
Celebrity
Football
Sports
Gen Z
Technology
Common Ground
RUN MY FRIEND
-husband Ben Affleck

--------------------------------------------------
RULES
--------------------------------------------------

The headline MUST:

• describe an event or discussion

• contain a verb whenever possible

• be natural English

• be between 3 and 8 words

• use Title Case

• avoid hashtags

• avoid emojis

• avoid quotation marks

• avoid clickbait

• avoid generic categories

• never be only a person's name

If a person appears,
describe WHAT happened.

--------------------------------------------------
Caption
--------------------------------------------------

{caption}

Return ONLY valid JSON.

{{
    "story_headline": "...",
    "confidence": 0.95
}}
"""

    @classmethod
    def resolve(cls, caption, candidates):

        if not caption:
            return None

        prompt = cls._build_prompt(
            caption,
            candidates
        )

        try:
            client = cls._get_client()
            raw = client.generate(prompt)

        except Exception as e:
            print(f"[LLM ERROR] {type(e).__name__}: {e}")
            return None

        cleaned = raw.strip()

        if cleaned.startswith("```"):
            cleaned = cleaned.replace("```json", "")
            cleaned = cleaned.replace("```", "").strip()

        try:
            data = json.loads(cleaned)

        except Exception:
            print("\nInvalid JSON returned:\n")
            print(cleaned)
            return None

        headline = data.get("story_headline")

        if not headline:
            return None

        headline = headline.strip()

        # Reject low-quality outputs so the pipeline falls back
        bad = {
            "Entertainment",
            "Sports",
            "Technology",
            "Politics",
            "Business",
            "Health",
            "Education",
            "Gen Z",
            "AI",
            "Marriage",
            "Celebrity",
            "Football",
            "Music"
        }

        if headline in bad:
            return None

        # Reject single-word headlines
        if len(headline.split()) < 2:
            return None

        return headline