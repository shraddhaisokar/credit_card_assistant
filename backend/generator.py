from backend.config import client, GROQ_MODEL

class Generator:
    def answer(self, question, context, history):

        # Build formatted conversation history (last 6 turns)
        history_text = ""
        for turn in history[-6:]:
            role = "User" if turn["role"] == "user" else "Bot"
            history_text += f"{role}: {turn['text']}\n"

        # Full assistant prompt (adapted from your original)
        prompt = f"""
You are a credit card assistant.

Conversation so far:
{history_text}

Instructions:
- Answer using the provided context.
- Give spaced out answers for readability.
- Keep answers conversational and user-friendly.
- Do NOT use markdown. Use plain text.
- If the user asks a follow-up question, use the conversation history.
- If the question is general (e.g., "What is a credit card?"), answer using your own knowledge.
- If the answer is not present in the context and cannot be inferred from history, say:
  "I do not have information about that."

Relevant document context:
{context}

User question:
{question}

Final answer:
"""

        # Call Groq LLM
        chat_completion = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful, knowledgeable credit card assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        # Return Groq response
        return chat_completion.choices[0].message.content
