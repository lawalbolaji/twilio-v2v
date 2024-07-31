from groq import Groq

from app.config.config import Settings
from .model import Model

settings = Settings()


class GroqClient(Model):
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY, max_retries=0, timeout=5)

    def complete(self, query: str):
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": """
                        You are a helpful assistant that helps with general knowledge questions.
                        You should prioritize the shortest answers that convey the point.
                        Your answers must never exceed 30 words under any circumstances.
                    """,
                },
                {
                    "role": "user",
                    "content": query,
                },
            ],
            model="llama-3.1-8b-instant",
        )

        return chat_completion.choices[0].message.content


# completion
