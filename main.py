
from brain.llm import JarvisBrain
from brain.personality import JARVIS_PERSONALITY
from database.memory import JarvisMemory


def main():

    print("=" * 50)
    print("             J.A.R.V.I.S.")
    print("       Just A Rather Very Intelligent System")
    print("=" * 50)

    print("\nInitializing AI systems...")

    # Initialize permanent memory
    memory = JarvisMemory()

    # Connect the memory system to JARVIS
    brain = JarvisBrain(JARVIS_PERSONALITY, memory)

    print("\nJARVIS is online.")
    print("Type a message to begin.")

    print("\nCommands:")
    print("  /remember key=value - Save a memory")
    print("  /recall             - Show all memories")
    print("  /recall key         - Recall one memory")
    print("  /forget key         - Delete a memory")
    print("  /clear              - Clear conversation history")
    print("  /quit               - Shut down JARVIS")

    while True:

        try:

            user_input = input("\nYou: ").strip()

            if not user_input:
                continue

            command = user_input.lower()

            if command == "/quit":
                print("\nJARVIS: Goodbye. Have a great day.")
                break

            elif command == "/clear":
                brain.clear_memory()
                print("\nJARVIS: Conversation history cleared.")
                continue

            elif command.startswith("/remember "):

                data = user_input[len("/remember "):]

                if "=" not in data:
                    print("\nJARVIS: Use this format: /remember key=value")
                    continue

                key, value = data.split("=", 1)

                try:
                    memory.save_memory(key, value)
                    print(f"\nJARVIS: I'll remember that {key.strip()} is {value.strip()}.")
                except ValueError as error:
                    print(f"\nJARVIS: {error}")

                continue

            elif command == "/recall":

                memories = memory.get_all_memories()

                if not memories:
                    print("\nJARVIS: I don't have any saved memories yet.")
                else:
                    print("\nJARVIS: Here is what I remember:")
                    for key, value in memories:
                        print(f"  {key}: {value}")

                continue

            elif command.startswith("/recall "):

                key = user_input[len("/recall "):].strip()
                value = memory.get_memory(key)

                if value is None:
                    print(f"\nJARVIS: I don't have a memory saved for '{key}'.")
                else:
                    print(f"\nJARVIS: {key} is {value}.")

                continue

            elif command.startswith("/forget "):

                key = user_input[len("/forget "):].strip()

                if not key:
                    print("\nJARVIS: Please specify a memory key.")
                    continue

                deleted = memory.delete_memory(key)

                if deleted:
                    print(f"\nJARVIS: I have forgotten '{key}'.")
                else:
                    print(f"\nJARVIS: I couldn't find a memory named '{key}'.")

                continue

            print("\nJARVIS is thinking...")

            response = brain.think(user_input)

            print(f"\nJARVIS: {response}")

        except KeyboardInterrupt:
            print("\n\nJARVIS: Shutting down. Goodbye.")
            break


if __name__ == "__main__":
    main()
