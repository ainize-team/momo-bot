import json
import discord
from discord import app_commands
from discord.ui import Button, View
import random

with open('emoji_dataset.json', 'r') as read_json:
    emoji_dataset = json.load(read_json)

# with open('hint_dataset.json', 'r') as read_json:
#     hint_dataset = json.load(read_json)

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False
        
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild=discord.Object(id=992003992009855026))
            self.synced = True
        print(f"We have logged in as {self.user}.")
        
client = aclient()
tree = app_commands.CommandTree(client)

user_movie = {}
user_hint = {}

@tree.command(name="quiz", description="Start a Quiz", guild=discord.Object(id=992003992009855026))
async def self(interaction: discord.Interaction):

    emoji_lst = list(emoji_dataset.keys())
    randnum = random.randrange(0, len(emoji_lst))
    emoji = emoji_lst[randnum]
    user_movie[interaction.user.id] = emoji_dataset[emoji]
    # user_hint[interaction.user.id] = hint_dataset[emoji_dataset[emoji]]

    embed = discord.Embed(title="Guess the movie, `" + str(interaction.user.name) + "`!", description="Use `/answer` to enter your answer", color=discord.Color.blue())
    embed.set_thumbnail(url=interaction.user.avatar)

    button = Button(label="Hint", style=discord.ButtonStyle.gray, emoji='🏳️')
    async def button_callback(interaction):
        # answer = user_hint[interaction.user.id]
        await interaction.response.send_message("<@" + str(interaction.user.id) + "> Hint: ??")
        # await interaction.response.send_message("<@" + str(interaction.user.id) + "> Hint: " + answer)
        
    button.callback = button_callback
    
    view = View()
    view.add_item(button)
    
    await interaction.response.send_message(emoji)
    await interaction.channel.send(embed=embed, view=view)
    
    return 

@tree.command(name="answer", description="Enter your answer", guild=discord.Object(id=992003992009855026))
async def self(interaction: discord.Interaction, answer: str):

    if interaction.user.id not in user_movie.keys():
        embed = discord.Embed(title="Use `/quiz` to start quiz first!", description="", color=discord.Color.red())
        embed.set_thumbnail(url=interaction.user.avatar)
        await interaction.response.send_message("<@" + str(interaction.user.id) + ">")
        await interaction.channel.send(embed=embed)
        return

    if answer == user_movie[interaction.user.id]:
        embed = discord.Embed(title="Answer is correct!", description="You got a **??** points", color=discord.Color.green())
        embed.set_thumbnail(url=interaction.user.avatar)
        embed.set_footer(text="Your score is ??")
        await interaction.response.send_message("<@" + str(interaction.user.id) + ">")
        await interaction.channel.send(embed=embed)
        
    else:
        embed = discord.Embed(title="Answer is wrong!", description="The answer is **" + user_movie[interaction.user.id] + "**", color=discord.Color.red())
        embed.set_thumbnail(url=interaction.user.avatar)
        embed.set_footer(text="Your score is ??")
        await interaction.response.send_message("<@" + str(interaction.user.id) + ">")
        await interaction.channel.send(embed=embed)
    
    del(user_movie[interaction.user.id])

    return 

client.run('')
