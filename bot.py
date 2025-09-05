import discord
from discord.ext import commands
import random
from discord import app_commands
import datetime
import os  # 環境変数読み込み用

# Intent設定
intents = discord.Intents.default()
intents.message_content = True  # メッセージ読み取りが必要な場合だけ

# Botの作成
bot = commands.Bot(command_prefix="", intents=intents)  # prefixは空でもOK

# 我に返ったときのセリフ
normal_lines = [
    "僕は何をしているんだろう……"
]

LOG_FILE = "command_logs.txt"

def log_command(user: discord.user, command: str, channel: discord.TextChannel):
    """コマンド入力をターミナルとtxtに記録"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {user} in #{channel} -> {command}"
    print(log_line)  # ターミナルに出す
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_line + "\n")  # txtに保存

# スラッシュコマンド
@bot.tree.command(name="tanaka", description="田中 くんに喋らせる")
async def say_tanaka(interaction: discord.Interaction, message: str):
    log_command(interaction.user, f"/tanaka {message}", interaction.channel)

    if random.randint(1, 10) == 1:  # 10分の1の確率
        reply = random.choice(normal_lines)
    else:  # 普通のときは入力内容も残す
        reply = message

    await interaction.response.send_message(reply)

# 起動時に同期
@bot.event
async def on_ready():
    await bot.tree.sync()  # スラッシュコマンドをDiscordに同期
    print(f"ログイン完了: {bot.user}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return  # 無視する
    raise error

# 環境変数からトークンを取得して起動
TOKEN = os.environ.get("DISCORD_TOKEN")
bot.run(TOKEN)