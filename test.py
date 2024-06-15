import random
from datetime import datetime, timedelta

users = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank"]
messages = [
    "Hey, what's up?",
    "Just got home. How about you?",
    "Can we meet tomorrow?",
    "LOL, that's hilarious!",
    "Did you finish the report?",
    "I'll call you in 5 minutes.",
    "Where are we going tonight?",
    "Happy Birthday!",
    "Sorry, I missed your call.",
    "Let's grab lunch sometime next week.",
    "Good morning! Have a great day! ",
    "Can you send me that file?",
    "What time does the meeting start?",
    "I'm running late, see you in 10 mins.",
    "How's your day going?",
    "Check out this cool video!",
    "Are you free this weekend?",
    "I can't make it tonight, sorry.",
    "Congratulations on your new job!",
    "Thanks for the help today.",
    "I'm at the mall, do you need anything?",
    "Do you know where to find good pizza?",
    "I'm so tired, need a nap.",
    "Got any plans for the holiday?",
    "Just finished my workout, feeling great!",
    "Can you believe what happened in the game?",
    "When are you coming over?",
    "Need any help with your project?",
    "Have you seen the latest movie?",
    "Let's go hiking this weekend.",
    "I'm stuck in traffic, ugh.",
    "What time are we meeting?",
    "Can you pick up some groceries?",
    "Just sent you an email, check it out.",
    "Got a new phone, loving it!",
    "I'm heading out now.",
    "Is everything okay?",
    "Don't forget our meeting tomorrow.",
    "Thanks for inviting me!",
    "That sounds like a great idea.",
    "Can you believe this weather?",
    "I'm cooking dinner tonight.",
    "I'll see you at the gym.",
    "How did your presentation go?",
    "Have a safe trip!",
    "What's the plan for tonight?",
    "I'm really busy right now.",
    "Let's catch up soon.",
    "I can't wait to see you!"
]


def generate_fake_whatsapp_chat():
    start_time = datetime.now() - timedelta(days=1)
    chat_lines = []

    for _ in range(50):
        timestamp = start_time.strftime("%H:%M")
        user = random.choice(users)
        message = random.choice(messages)
        chat_lines.append(f"{timestamp} - {user}: {message}")
        start_time += timedelta(minutes=random.randint(1, 5))

    return "\n".join(chat_lines)


fake_chat = generate_fake_whatsapp_chat()
with open("fake_whatsapp_chat.txt", "w") as file:
    file.write(fake_chat)

print(fake_chat)