import json
from backend.config import client, GROQ_MODEL

INTENTS = [
    "informational",
    "block_card",
    "check_balance",
    "convert_emi",
    "track_delivery",
    "download_statement",
    "dispute_transaction",
    "raise_complaint"
]

def classify_intent(query):

    prompt = f"""
You are an intent classifier for a credit card support chatbot.
If you are given a question to which you can respond with information, or for steps to achieve something , or for help, then classify it as "informational". Classify all questions as informational unless the user is explicitly asking you to perform an action.
Otherwise, if the user is explicitly asking you to perform an action, classify the question into one of the following intents. ONLY IF THE USER IS ASKING YOU TO DO SOMETHING.:

Valid intents: {INTENTS}

Return ONLY valid JSON in this exact format:
{{"intent": "<value>"}}

User query: "{query}"
"""

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": "You classify user queries into intents."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    text = response.choices[0].message.content


    try:
        parsed = json.loads(text)
        if parsed["intent"] in INTENTS:
            return parsed["intent"]
    except:
        pass

    # Default fallback
    return "informational"
