import json
import discord
from discord import app_commands
from discord.ui import Button, View
import random
from dotenv import load_dotenv
import os

load_dotenv()

with open('emoji_dataset.json', 'r', encoding='utf-8') as read_json:
    emoji_dataset = json.load(read_json)

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False
        
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild=discord.Object(id=int(os.environ.get('GUILD_ID'))))
            self.synced = True
        
client = aclient()
tree = app_commands.CommandTree(client)

@tree.command(name="quiz", description="Start a Quiz!", guild=discord.Object(id=int(os.environ.get('GUILD_ID'))))
async def self(interaction: discord.Interaction):
    
    n = int(os.environ.get('QUESTION'))
    samples = random.sample(list(emoji_dataset.keys()), n)
    answer_idx = random.randrange(0, n)
    answer_title = samples[answer_idx]
    answer_emoji = emoji_dataset[answer_title]

    embed = discord.Embed(title="Guess the movie!", description="Choose the movie you think is the correct answer.", color=discord.Color.blue())
    button1 = Button(label=samples[0], style=discord.ButtonStyle.gray, emoji='1️⃣')
    button2 = Button(label=samples[1], style=discord.ButtonStyle.gray, emoji='2️⃣')
    button3 = Button(label=samples[2], style=discord.ButtonStyle.gray, emoji='3️⃣')
    button4 = Button(label=samples[3], style=discord.ButtonStyle.gray, emoji='4️⃣')
    button5 = Button(label=samples[4], style=discord.ButtonStyle.gray, emoji='5️⃣')
    
    async def wrong_answer_button_callback(interaction):      
        embed = discord.Embed(title="❌", description="Try again!", color=discord.Color.red())
        embed.set_thumbnail(url=interaction.user.avatar)      
        await interaction.response.send_message("<@" + str(interaction.user.id) + ">")
        await interaction.channel.send(embed=embed)
        
    async def correct_answer_button_callback(interaction):      
        embed = discord.Embed(title="⭕", description="You answered correctly!\n\nUse `/quiz` to start a new quiz.", color=discord.Color.green())
        embed.set_thumbnail(url=interaction.user.avatar) 
        await interaction.response.send_message("<@" + str(interaction.user.id) + ">")
        await interaction.channel.send(embed=embed)
  
    if answer_idx == 0:        
        button1.callback = correct_answer_button_callback
        button2.callback = wrong_answer_button_callback
        button3.callback = wrong_answer_button_callback
        button4.callback = wrong_answer_button_callback
        button5.callback = wrong_answer_button_callback
      
    elif answer_idx == 1:        
        button1.callback = wrong_answer_button_callback
        button2.callback = correct_answer_button_callback
        button3.callback = wrong_answer_button_callback
        button4.callback = wrong_answer_button_callback
        button5.callback = wrong_answer_button_callback
        
    elif answer_idx == 2:        
        button1.callback = wrong_answer_button_callback
        button2.callback = wrong_answer_button_callback
        button3.callback = correct_answer_button_callback
        button4.callback = wrong_answer_button_callback
        button5.callback = wrong_answer_button_callback
        
    elif answer_idx == 3:        
        button1.callback = wrong_answer_button_callback
        button2.callback = wrong_answer_button_callback
        button3.callback = wrong_answer_button_callback
        button4.callback = correct_answer_button_callback
        button5.callback = wrong_answer_button_callback
        
    elif answer_idx == 4:        
        button1.callback = wrong_answer_button_callback
        button2.callback = wrong_answer_button_callback
        button3.callback = wrong_answer_button_callback
        button4.callback = wrong_answer_button_callback
        button5.callback = correct_answer_button_callback
        
    view = View()
    view.add_item(button1)
    view.add_item(button2)
    view.add_item(button3)
    view.add_item(button4)
    view.add_item(button5)
    
    await interaction.response.send_message(answer_emoji)
    await interaction.channel.send(embed=embed, view=view)
    
    return 

client.run(os.environ.get('TOKEN'))