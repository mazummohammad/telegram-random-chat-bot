# telegram-random-chat-bot
telegram-random-chat-bot is a Telegram bot that connects strangers for anonymous, random 1-on-1 conversations. Users can start chatting with a single command, and the bot automatically pairs them with another active user. No registration, no personal info — just simple and secure random chatting.

🚀 Features
-🔄 Random matchmaking — pairs users automatically
-💬 Anonymous chat — hides usernames and personal details
-▶️ Easy commands — /start, /next, /stop
-🧠 Session management — handles active chat queues
-🛡️ Privacy-friendly — no user data stored
-⚙️ Customizable — easy to extend with new features

🧩 How it Works
-User sends /start
-The bot adds them to a queue
-When another user joins, both are matched
-Messages are forwarded between them
-/stop ends the session
-/next finds a new partner immediately

🛠️ Tech Stack
-Python
-python-telegram-bot / TeleBot / Pyrogram (depending on your implementation)
-Simple in-memory or DB-based matchmaking system
