import os
import discord
from keepAlive import keep_alive

# Import Files
from functions.utils import get_quote, show_commands, contains_number, does_user_exist
from functions.actions import update_status, view_all, delete_goal, my_goals, insert_goal_to_db

# initializations
client = discord.Client()

########################################
  # Runs on start & on each message
########################################
@client.event
async def on_ready(): 
  print('We have logged in as {0.user}'.format(client))
  
@client.event
async def on_message(message):
  if (message.author == client.user): return
    
  if (message.content.startswith('$new ')):
    await insert_goal_to_db(message)
    
  elif (message.content.lower().startswith('$inspire')):
    await message.channel.send(get_quote())
    
  elif (message.content.startswith('$all')):
    await view_all(message)

  elif (message.content.lower().startswith('$commands')):
      await show_commands(message)

  elif (message.content.startswith('$goals')):
    if (await does_user_exist(message) == False): 
      return
    await my_goals(message)

  elif (message.content.lower().startswith('$update ')):
    if (await does_user_exist(message) == False): 
      return
    
    if ((("done" in message.content.lower()) or ("in progress" in message.content.lower())) and contains_number(message.content)):
      await update_status(message)
    else:
      await message.channel.send("⚠️ ERROR: missing status or digit- Example: *$update 3 in progress*")
      
  elif (message.content.lower().startswith('$delete')):
    if (await does_user_exist(message) == False): 
      return
    if (message.content.lower() == '$delete' or message.content.lower() == '$delete ' ):
      await message.channel.send('⚠️ ERROR: To delete a goal you must include the goal number. Example: *$delete 3* ') 
    else:
      await message.channel.send('deleting ...') 
      await delete_goal(message)
      
try:
    keep_alive()
    client.run(os.environ['DISCORD_TOKEN']) 
except:
    os.system("kill 1")
