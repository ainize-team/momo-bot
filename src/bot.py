import asyncio
import json
import random

import discord
import firebase_admin
from discord import app_commands
from discord.ui import Button, View
from firebase_admin import credentials
from loguru import logger

from settings import discord_settings, firebase_settings
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
cred = credentials.Certificate(firebase_settings.cred_path)
firebase_admin.initialize_app(cred, {"databaseURL": firebase_settings.database_url})


@tree.command(
    name="quiz",
    description="Start a Quiz!",
    guild=discord.Object(id=discord_settings.guild_id),
)
async def quiz(interaction: discord.Interaction):
    quiz_id = interaction.id

    number_emoji_list = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
    n = len(number_emoji_list)
    samples = random.sample(list(emoji_dataset.keys()), n)
    answer_idx = random.randrange(0, n)
    answer_title = samples[answer_idx]
    answer_emoji = emoji_dataset[answer_title]

    save_quiz_info(quiz_id, answer_title, answer_emoji)

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
        user_id = user.id

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
        user_id = user.id

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

        button = Button(label="leaderboard", style=discord.ButtonStyle.gray, emoji="🏆")

        async def button_callback(interaction: discord.Interaction):
            description = ""
            for step in range(50):
                leaderboard = get_leaderboard(quiz_id)
                if leaderboard is None:
                    logger.info(f"{step}/50")
                    await asyncio.sleep(0.5)
                else:
                    break

            for rank, (user_id, data) in enumerate(leaderboard, start=1):
                num_solved_quiz = data["num_solved_quiz"]
                num_attempt_quiz = data["num_attempt_quiz"]

                if rank == 1:
                    prefix = "🥇"
                elif rank == 2:
                    prefix = "🥈"
                elif rank == 3:
                    prefix = "🥉"
                else:
                    prefix = "`{rank}`"

                user_info = f"<@{user_id}>({num_solved_quiz}/{num_attempt_quiz})"
                description = f"{prefix} {user_info}\n"

            embed = discord.Embed(
                title="**Top 10**",
                description=description,
                color=discord.Color.green(),
            )

            await interaction.response.send_message(embed=embed, ephemeral=True)

        button.callback = button_callback
        view = View(timeout=None)
        view.add_item(button)

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


client.run(discord_settings.token)
