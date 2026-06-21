# ============================================================
#   PatternBot - A Beginner-Level Chatbot in Python
#   Uses: re (regex), random — no external libraries needed!
# ============================================================

import re
import random

# ─── Step 1: Define patterns and responses ───────────────────
# Each rule is a list: [regex_pattern, [list of possible responses]]
# The bot picks a random response from the list each time.

rules = [

    # Greetings
    [r"hi|hello|hey|howdy",
     ["Hello! How are you?",
      "Hey there! 👋",
      "Hi! Nice to meet you!"]],

    # Farewell
    [r"bye|goodbye|see you|exit|quit",
     ["Goodbye! Have a great day! 👋",
      "See you later!",
      "Bye bye! Take care!"]],

    # How are you
    [r"how are you|how r u|how are u",
     ["I'm doing great, thanks for asking!",
      "Feeling good! How about you?",
      "All good on my end! 😊"]],

    # Name
    [r"what is your name|who are you|your name",
     ["I'm PatternBot, a simple chatbot built with Python!",
      "My name is PatternBot. Nice to meet you!"]],

    # Tell a joke
    [r"joke|tell me something funny|make me laugh",
     ["Why don't scientists trust atoms? Because they make up everything! 😄",
      "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
      "What do you call a fake noodle? An impasta! 🍝"]],

    # Age
    [r"how old are you|your age",
     ["I'm ageless! I was just created. 😄",
      "Age is just a number for bots!"]],

    # Thank you
    [r"thanks|thank you|thx|ty",
     ["You're welcome! 😊",
      "Anytime! Happy to help.",
      "My pleasure!"]],

    # What can you do
    [r"what can you do|help|your features",
     ["I can chat with you, tell jokes, and answer simple questions!",
      "Try asking me a joke, my name, or just say hello!"]],

    # Favourite color
    [r"favourite color|favorite color|your color",
     ["I love the color blue 💙 — like the sky!",
      "I'd say purple 💜 — it feels like magic!"]],

    # Weather (simple response, no API)
    [r"weather|is it raining|is it sunny",
     ["I can't check real weather, but I hope it's sunny for you! ☀️",
      "No live data here, but stay prepared! 🌂"]],
]

# ─── Step 2: Match input to a rule ───────────────────────────

def get_response(user_input):
    # Convert input to lowercase so matching is case-insensitive
    user_input = user_input.lower()

    for pattern, responses in rules:
        # re.search checks if the pattern exists anywhere in the input
        if re.search(pattern, user_input):
            return random.choice(responses)  # Pick a random response

    # If nothing matched, return a default fallback
    return random.choice([
        "Hmm, I didn't understand that. Can you rephrase? 🤔",
        "I'm not sure about that one. Try asking something else!",
        "That one stumped me! Ask me a joke maybe? 😄"
    ])

# ─── Step 3: Main chat loop ──────────────────────────────────

def main():
    print("=" * 45)
    print("   Welcome to PatternBot! 🤖")
    print("   Type 'bye' or 'quit' to exit.")
    print("=" * 45)
    print()

    while True:
        # Get input from the user
        user_input = input("You: ").strip()

        # Skip empty input
        if not user_input:
            continue

        # Get the bot's response
        response = get_response(user_input)
        print(f"Bot: {response}")
        print()

        # Exit if the user said goodbye
        if re.search(r"bye|goodbye|exit|quit", user_input.lower()):
            break

# ─── Run the chatbot ─────────────────────────────────────────

if __name__ == "__main__":
    main()
