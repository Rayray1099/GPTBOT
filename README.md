# GPTBOT

This is a simple Discord bot that chats with users using the gpt-4o-mini model hosted at `https://free.v36.cm/v1/`.

## Features
- Mention the bot (`@BotName <message>`) or reply to one of its messages to chat.
- Conversation memory is kept per user in memory.
- Use the `/settings` slash command to set a custom system prompt. A modal will appear so you can enter the prompt.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set the following environment variables:
   - `DISCORD_TOKEN` – your Discord bot token.
   - `V36_API_KEY` – API key for `https://free.v36.cm/v1/` (e.g. `sk-R8DUcZbUg7kHYSb6D3D3C9Ce798142F8AdC74f1eAa966881`).
3. Run the bot:
   ```bash
   python bot.py
   ```

The bot will register the `/settings` command when it starts. Use `@BotName` mentions or reply to its messages to talk with memory.
