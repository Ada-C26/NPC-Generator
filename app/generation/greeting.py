import json
from google import genai

client = genai.Client()

GREETING_PROMPT = """
You are a system that generates greeting suggestions for an NPC character for a role-playing game based on structured input.

RESPONSE FORMAT RULES (follow these exactly):
1. You must respond with JSON only.
2. The JSON must be a single object with exactly one key: "greetings".
3. The value of "greetings" must be an array containing exactly 10 strings.
4. Each string must be a unique greeting suggestion.
5. Do not include any text before or after the JSON object.
6. Do not include comments, explanations, apologies, or descriptions.
7. Your response must be valid JSON that can be parsed without modification.

EXAMPLES (learn the pattern exactly):

Request: {{"name": "Liora Maplewind", "age": 14, "occupation": "Aspiring Pokémon Ranger", "personality": "Energetic, compassionate, and endlessly curious."}}
Response:
{{"greetings": [
    "Hi there! Want to explore the woods with me? I heard rare Pokémon live nearby!",
    "Oh! Let me help you—are your Pokémon hurt? I always carry supplies!",
    "Wow, your partner looks amazing! Mind if I sketch them in my journal?"
]}}

Request: {{"name": "Darren Valenshard", "age": 27, "occupation": "Crystalbound Knight", "personality": "Stoic, honorable, and introspective."}}
Response:
{{"greetings": [
    "Stay vigilant—these lands are not as peaceful as they appear.",
    "Traveler, may the crystals guide your path. What brings you here?",
    "If you seek strength, I can offer training… though my methods are not easy."
]}}

NOW COMPLETE THE FOLLOWING:

Request: {{"name": "{name}", "age": "{age}", "occupation": "{occupation}", "personality": "{personality}"}}
Response:
"""

def generate_greetings(character):
    # input_message = f"I am writing a fantasy RPG video game. I have an npc named {character.name} who is {character.age} years old. They are a {character.occupation} who has a {character.personality} personality. Please generate a Python style list of 10 stock phrases they might use when the main character talks to them. Please return just the list without a variable name and square brackets."

    input_message = GREETING_PROMPT.format(
        name=character.name,
        age=character.age,
        occupation=character.occupation,
        personality=character.personality,
    )

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite", contents=input_message
    )

    try:
        result = json.loads(response.text)
    except json.decoder.JSONDecodeError:
        return []

    print(result)
    return result["greetings"]
