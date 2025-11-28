import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = "8551196596:AAFlWWc4BIVTnq2YSU6tZ6itqPF4kYKOIjo"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# -----------------------
# Data storage
# -----------------------
waiting_users = []          # users waiting for chat
active_pairs = {}           # user_id -> partner_id


# -----------------------
# Helper functions
# -----------------------
async def pair_users(user1, user2):
    active_pairs[user1] = user2
    active_pairs[user2] = user1

    await bot.send_message(user1, "🔥 You are now connected to a stranger!\nSend /stop to end chat.")
    await bot.send_message(user2, "🔥 You are now connected to a stranger!\nSend /stop to end chat.")


async def stop_chat(user_id):
    if user_id in active_pairs:
        partner = active_pairs[user_id]
        await bot.send_message(partner, "❌ The stranger left the chat.")
        await bot.send_message(user_id, "❌ You left the chat.")

        # remove pair
        del active_pairs[partner]
        del active_pairs[user_id]


# -----------------------
# Commands
# -----------------------
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 Welcome to Random Chat!\n"
        "Use /next to connect with a random stranger.\n"
        "Use /stop to end the chat."
    )


@dp.message(Command("next"))
async def next_cmd(message: types.Message):
    user_id = message.from_user.id

    # If user is in a chat, stop it first
    if user_id in active_pairs:
        await stop_chat(user_id)

    # If someone is waiting, pair with them
    if waiting_users and waiting_users[0] != user_id:
        partner = waiting_users.pop(0)
        await pair_users(partner, user_id)
    else:
        # Put user in waiting list
        if user_id not in waiting_users:
            waiting_users.append(user_id)
        await message.answer("⏳ Waiting for a stranger...")


@dp.message(Command("stop"))
async def stop(message: types.Message):
    await stop_chat(message.from_user.id)


# -----------------------
# Forward messages between paired users
# -----------------------
@dp.message()
async def relay(message: types.Message):
    user_id = message.from_user.id

    if user_id in active_pairs:
        partner = active_pairs[user_id]

        # forward messages (text only now)
        if message.text:
            await bot.send_message(partner, message.text)
        elif message.photo:
            await bot.send_photo(partner, message.photo[-1].file_id)
        elif message.sticker:
            await bot.send_sticker(partner, message.sticker.file_id)
        else:
            await bot.send_message(partner, "⚠ Unsupported message type.")
    else:
        await message.answer("❗ You are not connected.\nSend /next to find a stranger.")


# -----------------------
# Run bot
# -----------------------
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
