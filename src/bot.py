import json
import os
import random

import discord
from discord import app_commands
from discord.ui import Button, View


with open("./emoji_dataset.json", "r", encoding="utf-8") as read_json:
    emoji_dataset = json.load(read_json)


class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild=discord.Object(id=int(os.environ.get("GUILD_ID"))))
            self.synced = True


client = aclient()
tree = app_commands.CommandTree(client)


@tree.command(
    name="quiz",
    description="Start a Quiz!",
    guild=discord.Object(id=int(os.environ.get("GUILD_ID"))),
)
async def self(interaction: discord.Interaction):
    number_emoji_list = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
    n = 5
    samples = random.sample(list(emoji_dataset.keys()), n)
    answer_idx = random.randrange(0, n)
    answer_title = samples[answer_idx]
    answer_emoji = emoji_dataset[answer_title]

    embed = discord.Embed(
        title="Guess the movie!",
        description="Choose the one that seems to be the correct answer from the examples.",
        color=discord.Color.blue(),
    )
    button_list = [
        Button(label=samples[i], style=discord.ButtonStyle.gray, emoji=number_emoji_list[i]) for i in range(5)
    ]

    async def wrong_answer_button_callback(interaction):
        embed = discord.Embed(
            title="❌",
            description="You answered wrong!\n\nChoose the one that seems to be the correct answer from the other examples.",
            color=discord.Color.red(),
        )
        if interaction.user.avatar is None:
            embed.set_thumbnail(url=interaction.user.default_avatar)
        else:
            embed.set_thumbnail(url=interaction.user.avatar)
        await interaction.response.send_message("<@" + str(interaction.user.id) + ">")
        await interaction.channel.send(embed=embed)

    async def correct_answer_button_callback(interaction):
        embed = discord.Embed(
            title="⭕",
            description="You answered correct!\n\nUse `/quiz` to start a new quiz.",
            color=discord.Color.green(),
        )
        if interaction.user.avatar is None:
            embed.set_thumbnail(url=interaction.user.default_avatar)
        else:
            embed.set_thumbnail(url=interaction.user.avatar)
        await interaction.response.send_message("<@" + str(interaction.user.id) + ">")
        await interaction.channel.send(embed=embed)

    view = View()
    for i in range(5):
        if i == answer_idx:
            button_list[i].callback = correct_answer_button_callback
        else:
            button_list[i].callback = wrong_answer_button_callback
        view.add_item(button_list[i])

    await interaction.response.send_message(answer_emoji)
    await interaction.channel.send(embed=embed, view=view)


client.run(os.environ.get("TOKEN"))
