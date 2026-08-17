import json
import os
import random

from google import genai


def load_quotes():
    with open("quotes.json", "r", encoding="utf-8") as file:
        return json.load(file)


def generate_content():

    quotes = load_quotes()

    quote = random.choice(quotes)

    client = genai.Client(
        api_key=os.environ["GEMINI_API_KEY"]
    )

    prompt = f"""
You are the content manager for a high-quality Instagram page
dedicated to Swami Vivekananda.

Create today's Instagram post using ONLY this verified quote:

"{quote['quote']}"

Theme:
{quote['theme']}

IMPORTANT RULES:

1. Never invent or modify the quote.
2. Never claim that Swami Vivekananda said anything other than the supplied quote.
3. Write a genuine, thoughtful caption.
4. Do not sound like generic AI motivational content.
5. Explain the practical meaning of the quote for a modern person.
6. Keep the caption around 100-180 words.
7. Use natural English.
8. Do not overuse emojis.
9. Generate 8-12 relevant hashtags.
10. Suggest a visual concept for a 1080x1350 Instagram post.
11. The visual concept should feel spiritual, powerful and premium.
12. Avoid cheesy designs and excessive text.

Return ONLY valid JSON in this exact structure:

{{
    "caption": "...",
    "hashtags": ["...", "..."],
    "visual_concept": "...",
    "quote": "{quote['quote']}",
    "theme": "{quote['theme']}"
}}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )

    text = response.text.strip()

    # Remove accidental markdown fences
    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    result = json.loads(text)

    return result
