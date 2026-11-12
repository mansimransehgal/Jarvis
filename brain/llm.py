
import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5:3b"


class JarvisBrain:

    def __init__(self, personality, memory=None):
        self.personality = personality
        self.memory = memory
        self.history = []

    def think(self, user_message):

        self.history.append({
            "role": "user",
            "content": user_message
        })

        # Load saved memories before generating a response
        memories = self.memory.get_all_memories() if self.memory else []

        memory_context = ""

        if memories:
            memory_context = "\n\nSAVED USER MEMORIES:\n"
            for key, value in memories:
                memory_context += f"- {key}: {value}\n"

            memory_context += (
                "\nUse these memories when relevant. "
                "Do not invent additional personal facts."
            )

        messages = [
            {
                "role": "system",
                "content": self.personality + memory_context
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
            self.history.pop()
            return "I cannot connect to my local AI brain. Is Ollama running?"

        except requests.exceptions.Timeout:
            self.history.pop()
            return "My response is taking too long. Please try again."

        except requests.exceptions.RequestException as error:
            self.history.pop()
            return f"I encountered an AI connection error: {error}"

    def clear_memory(self):
        """Clear temporary conversation history."""
        self.history.clear()
