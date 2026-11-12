
from brain.llm import JarvisBrain
from brain.personality import JARVIS_PERSONALITY


def main():

    print("=" * 50)
    print("             J.A.R.V.I.S.")
    print("       Just A Rather Very Intelligent System")
    print("=" * 50)

    print("\nInitializing AI systems...")

    brain = JarvisBrain(JARVIS_PERSONALITY)

    print("\nJARVIS is online.")
    print("Type a message to begin.")
    print("\nCommands:")
    print("  /clear  - Clear conversation memory")
    print("  /quit   - Shut down JARVIS")

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
                print("\nJARVIS: Conversation memory cleared.")
                continue

            print("\nJARVIS is thinking...")

            response = brain.think(user_input)

            print(f"\nJARVIS: {response}")

        except KeyboardInterrupt:
            print("\n\nJARVIS: Shutting down. Goodbye.")
            break


if __name__ == "__main__":
    main()
