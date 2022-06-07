import requests
import json
import discord

from functions.actions import collection

# inspirational quotes
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " - " + json_data[0]['a']
  return (quote)

# commands
async def show_commands(goalInput):
  embed = discord.Embed(title="__Commands__", color= discord.Colour.purple())
  embed.add_field(name="Add your own goal: *$new {msg}*", value="Example: $new I want to learn to code!", inline=False)
  embed.add_field(name="View your own goals: *$goals*", value="Example: $goals", inline=False)
  embed.add_field(name="View everyone's goals: *$all*", value="Example: $all", inline=False)
  embed.add_field(name="Update specified goal: *$update {#} {status}*", value="Example: $update 4 done \nExample: $update 3 in progress", inline=False)
  embed.add_field(name="Delete specified goal: *$delete {#}*", value="Example: $delete 2", inline=False)
  embed.add_field(name="Sends a zen quote: *$inspire*", value="Example: $inspire", inline=False)

  await goalInput.channel.send(embed=embed)

# number check
def contains_number(value):
  return any(character.isdigit() for character in value)

# user exists check
async def does_user_exist(goalInput):
   userId = goalInput.author.id
   if (collection.count_documents({"userId" : userId}, limit = 1) == 0):
     await goalInput.channel.send("⚠️ ERROR: Looks like you're trying to view, edit, or delete goal(s) that dont exist. Enter *$commands* for help")
     return (False)
   else:
     return (True)
