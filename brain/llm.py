
import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5:3b"


class JarvisBrain:

    def __init__(self, personality):
        self.personality = personality
        self.history = []

    def think(self, user_message):

        self.history.append({
            "role": "user",
            "content": user_message
        })

        messages = [
            {
                "role": "system",
                "content": self.personality
            }
        ] + self.history

        try:
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": MODEL,
                    "messages": messages,
                    "stream": False
                },
                timeout=180
            )

            response.raise_for_status()

            answer = response.json()["message"]["content"]

            self.history.append({
                "role": "assistant",
                "content": answer
            })

            return answer

        except requests.exceptions.ConnectionError:
            return "I cannot connect to my local AI brain. Is Ollama running?"

        except requests.exceptions.Timeout:
            return "My response is taking too long. Please try again."

        except requests.exceptions.RequestException as error:
            return f"I encountered an AI connection error: {error}"

    def clear_memory(self):
        self.history.clear()
