import os
import discord
from discord.ext import commands
import aiohttp

API_URL = "https://free.v36.cm/v1/chat/completions"
API_KEY = os.getenv("V36_API_KEY")
MODEL = "gpt-4o-mini"

default_prompt = "You are a helpful assistant."

# conversation history per user
conversations = {}
# custom system prompt per user
user_prompts = {}

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


def build_messages(user_id, content):
    prompt = user_prompts.get(user_id, default_prompt)
    history = conversations.setdefault(user_id, [])
    history.append({"role": "user", "content": content})
    # keep last 20 exchanges
    history[:] = history[-20:]
    messages = [{"role": "system", "content": prompt}] + history
    return messages

async def query_openai(messages):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "messages": messages,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, json=payload, headers=headers) as resp:
            data = await resp.json()
            return data["choices"][0]["message"]["content"]

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@bot.tree.command(name="settings", description="Set system prompt")
async def settings_command(interaction: discord.Interaction):
    class PromptModal(discord.ui.Modal, title="Set System Prompt"):
        prompt = discord.ui.TextInput(label="System Prompt", style=discord.TextStyle.paragraph)
        async def on_submit(self, inter: discord.Interaction):
            user_prompts[inter.user.id] = self.prompt.value
            await inter.response.send_message("System prompt updated.", ephemeral=True)
    await interaction.response.send_modal(PromptModal())

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    await bot.process_commands(message)
    mention = bot.user.mention
    should_respond = False
    content = message.content
    if mention in content:
        content = content.replace(mention, "").strip()
        should_respond = True
    elif message.reference and message.reference.resolved and message.reference.resolved.author == bot.user:
        should_respond = True
    if not should_respond:
        return
    messages = build_messages(message.author.id, content)
    try:
        reply = await query_openai(messages)
        conversations[message.author.id].append({"role": "assistant", "content": reply})
        await message.reply(reply)
    except Exception as e:
        await message.reply(f"Error: {e}")

if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not API_KEY or not token:
        raise RuntimeError("DISCORD_TOKEN and V36_API_KEY must be set")
    bot.run(token)
