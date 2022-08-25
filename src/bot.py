import json
import os
import random
import time
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

quiz_leaderboard = {} # TODO: 봇이 재시작하면 리더보드가 초기화되는데, 

@tree.command(
    name="quiz",
    description="Start a Quiz!",
    guild=discord.Object(id=int(os.environ.get("GUILD_ID"))),
)
async def self(interaction: discord.Interaction):

    quiz_id = interaction.id
    quiz_leaderboard[quiz_id] = list()

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
        Button(label=samples[i], style=discord.ButtonStyle.gray, emoji=number_emoji_list[i]) for i in range(n)
    ]

    async def wrong_answer_button_callback(interaction):

        if str(interaction.user) in quiz_leaderboard[quiz_id]:
            embed = discord.Embed(
                title="🚫",
                description="You have already solved the quiz.",
                color=discord.Color.red(),
            )
            if interaction.user.avatar is None:
                embed.set_thumbnail(url=interaction.user.default_avatar)
            else:
                embed.set_thumbnail(url=interaction.user.avatar)
            message = await interaction.response.send_message(embed=embed, ephemeral=True)
            time.sleep(10)
            await message.delete()

            return

        embed = discord.Embed(
            title="❌",
            description="You answered wrong!\n\nChoose the one that seems to be the correct answer from the other examples.",
            color=discord.Color.red(),
        )
        if interaction.user.avatar is None:
            embed.set_thumbnail(url=interaction.user.default_avatar)
        else:
            embed.set_thumbnail(url=interaction.user.avatar)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def correct_answer_button_callback(interaction):
        
        if str(interaction.user) in quiz_leaderboard[quiz_id]:
            embed = discord.Embed(
                title="🚫",
                description="You have already solved the quiz.",
                color=discord.Color.red(),
            )
            if interaction.user.avatar is None:
                embed.set_thumbnail(url=interaction.user.default_avatar)
            else:
                embed.set_thumbnail(url=interaction.user.avatar)
            await interaction.response.send_message(embed=embed, ephemeral=True)

            return

        quiz_leaderboard[quiz_id].append(str(interaction.user))
        
        embed = discord.Embed(
            title="⭕",
            description="You answered correct!\n\nUse `/quiz` to start a new quiz.",
            color=discord.Color.green(),
        )
        if interaction.user.avatar is None:
            embed.set_thumbnail(url=interaction.user.default_avatar)
        else:
            embed.set_thumbnail(url=interaction.user.avatar)

        button = Button(label="leaderboard", style=discord.ButtonStyle.gray, emoji="🏆")

        async def button_callback(interaction):
            rank = 1
            description = ""
            for user in quiz_leaderboard[quiz_id]:
                if rank == 11: break

                if rank == 1: description += "🥇 " + user + "\n"
                elif rank == 2: description += "🥈 " + user + "\n"
                elif rank == 3: description += "🥉 " + user + "\n"
                else: description += "`" + str(rank) + " ` " + user + "\n"
                rank += 1

            embed = discord.Embed(
                title="**Top 10**",
                description=description,
                color=discord.Color.green(),
            )

            await interaction.response.send_message(embed=embed, ephemeral=True)
            
        button.callback = button_callback
        view = View()
        view.add_item(button)

        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    view = View()
    for i in range(n):
        if i == answer_idx:
            button_list[i].callback = correct_answer_button_callback
        else:
            button_list[i].callback = wrong_answer_button_callback
        view.add_item(button_list[i])

    await interaction.response.send_message(answer_emoji)
    await interaction.channel.send(embed=embed, view=view)

client.run(os.environ.get("TOKEN"))
