import json
import random

import discord
import firebase_admin
from discord import app_commands
from discord.ui import Button, View
from firebase_admin import credentials
from loguru import logger

from settings import discord_settings, firebase_cred_settings, firebase_settings
from utils import get_leaderboard, is_quiz_solved, save_attempt_quiz_info, save_quiz_info, save_solved_quiz_info


with open("./emoji_dataset.json", "r", encoding="utf-8") as read_json:
    emoji_dataset = json.load(read_json)


class MomoBotClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild=discord.Object(id=discord_settings.guild_id))
            self.synced = True
        logger.info(f"Bot({self.user}) is logged in.")


client = MomoBotClient()
tree = app_commands.CommandTree(client)

# Firebase Initialization
cred = credentials.Certificate(
    {
        "type": firebase_cred_settings.type,
        "project_id": firebase_cred_settings.project_id,
        "private_key_id": firebase_cred_settings.private_key_id,
        "private_key": firebase_cred_settings.private_key.replace("\\n", "\n"),
        "client_email": firebase_cred_settings.client_email,
        "client_id": firebase_cred_settings.client_id,
        "auth_uri": firebase_cred_settings.auth_uri,
        "token_uri": firebase_cred_settings.token_uri,
        "auth_provider_x509_cert_url": firebase_cred_settings.auth_provider_x509_cert_url,
        "client_x509_cert_url": firebase_cred_settings.client_x509_cert_url,
    }
)
firebase_admin.initialize_app(cred, {"databaseURL": firebase_settings.database_url})


@tree.command(
    name="quiz",
    description="Start a Quiz!",
    guild=discord.Object(id=discord_settings.guild_id),
)
async def quiz(interaction: discord.Interaction):
    number_emoji_list = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
    n = len(number_emoji_list)
    samples = random.sample(list(emoji_dataset.keys()), n)
    answer_idx = random.randrange(0, n)
    answer_title = samples[answer_idx]
    answer_emoji = emoji_dataset[answer_title]

    quiz_id = save_quiz_info(answer_title, answer_emoji)

    embed = discord.Embed(
        title="Guess the movie!",
        description="Choose the one that seems to be the correct answer from the examples.",
        color=discord.Color.blue(),
    )

    button_list = [
        Button(label=samples[i], style=discord.ButtonStyle.gray, emoji=number_emoji_list[i]) for i in range(n)
    ]

    async def wrong_answer_button_callback(interaction: discord.Interaction):
        user = interaction.user
        user_id = str(user.id)

        if is_quiz_solved(quiz_id, user_id):
            embed = discord.Embed(
                title="🚫",
                description="You have already solved the quiz.",
                color=discord.Color.red(),
            )
            if user.avatar is None:
                embed.set_thumbnail(url=user.default_avatar)
            else:
                embed.set_thumbnail(url=user.avatar)
            await interaction.response.send_message(embed=embed, ephemeral=True)

            return

        embed = discord.Embed(
            title="❌",
            description="You answered wrong!\n\nChoose the one that seems to be the correct answer from the other examples.",
            color=discord.Color.red(),
        )
        if user.avatar is None:
            embed.set_thumbnail(url=user.default_avatar)
        else:
            embed.set_thumbnail(url=user.avatar)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        save_attempt_quiz_info(quiz_id, user_id)

    async def correct_answer_button_callback(interaction: discord.Interaction):
        user = interaction.user
        user_id = str(user.id)

        if is_quiz_solved(quiz_id, user_id):
            embed = discord.Embed(
                title="🚫",
                description="You have already solved the quiz.",
                color=discord.Color.red(),
            )
            if user.avatar is None:
                embed.set_thumbnail(url=user.default_avatar)
            else:
                embed.set_thumbnail(url=user.avatar)
            await interaction.response.send_message(embed=embed, ephemeral=True)

            return

        embed = discord.Embed(
            title="⭕",
            description="You answered correct!\n\nUse `/quiz` to start a new quiz.",
            color=discord.Color.green(),
        )
        if user.avatar is None:
            embed.set_thumbnail(url=user.default_avatar)
        else:
            embed.set_thumbnail(url=user.avatar)

        view = View(timeout=None)

        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        save_solved_quiz_info(quiz_id, user_id)

    view = View(timeout=None)
    for i in range(n):
        if i == answer_idx:
            button_list[i].callback = correct_answer_button_callback
        else:
            button_list[i].callback = wrong_answer_button_callback
        view.add_item(button_list[i])

    await interaction.response.send_message(answer_emoji)
    await interaction.channel.send(embed=embed, view=view)


@tree.command(
    name="leaderboard",
    description="Show MOMO Quiz Leaderboard!",
    guild=discord.Object(id=discord_settings.guild_id),
)
async def leaderboard(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    description = ""
    leaderboard = get_leaderboard()

    if leaderboard is None:
        description = "No one is on the leaderboard yet."
        title = "**Leaderboard**"
    else:
        leaderboard = leaderboard.records
        title = "**Leaderboard**(Solved/Attempted)"
        for rank, data in enumerate(leaderboard, start=1):
            user_id = str(data.user_id)
            num_solved_quiz = data.num_solved_quiz
            num_attempt_quiz = data.num_attempt_quiz

            if rank == 1:
                prefix = "🥇"
            elif rank == 2:
                prefix = "🥈"
            elif rank == 3:
                prefix = "🥉"
            else:
                prefix = f"`{rank}`"

            user_info = f"<@{user_id}>({num_solved_quiz}/{num_attempt_quiz})"
            description += f"{prefix} {user_info}\n"

    embed = discord.Embed(
        title=title,
        description=description,
        color=discord.Color.green(),
    )

    await interaction.response.send_message(embed=embed)


client.run(discord_settings.token)
