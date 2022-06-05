import requests
import json
from pymongo import MongoClient
import os
import discord
import datetime

# Import Files
import classDefn

# mongo db connection
cluster = MongoClient('mongodb+srv://samanthatb1:{}@cluster0.exbe3.mongodb.net/?retryWrites=true&w=majority'.format(os.environ['MONGO_PASS']))
database = cluster["WiEDiscord"]
collection = database["goals"]

# UPDATE STATUS
async def update_status(goalInput):
  userId = goalInput.author.id
  input = goalInput.content.split(' ')
  goalToUpdateId = int(input[1].replace(" ", ""))
  dbEntry = collection.find_one({"userId" : userId})
  totalGoals = dbEntry["totalGoalsNumber"]
  goalArray = dbEntry["goals"]

  if (goalToUpdateId <= 0 or goalToUpdateId > totalGoals):
    await goalInput.channel.send("⚠️ ERROR: Sorry, that goal number doesn't seem to exist")
    return
    
  if ("in progress" in goalInput.content.lower()):
    newStatus = "IN PROGRESS 🕑"
  else:
    newStatus = "DONE ✅"
  print("changing status to", newStatus)

  #find the array entry thats the # they wanna update
  for goal in goalArray:
    if(goal["number"] == goalToUpdateId):
      goal["status"] = newStatus
      break
    
  collection.update_one({"userId" : userId}, { "$set": { "goals": goalArray} })
  await my_goals(goalInput)

  
# DISPLAY ALL GOALS
async def view_all(goalInput):
  embed = discord.Embed(title="__View Everyone's Goals__", color= discord.Colour.purple())
  embed.set_footer(text="Type $commands for a list of commands")

  for user in collection.find():
     goalFormat = " "
     for goal in user["goals"]: 
       goalFormat = goalFormat + goal["message"] + " : " + goal["status"] + "\n"
     embed.add_field(name="{}".format(user["username"]), value= goalFormat, inline=False)

  embed.add_field(name="\u200b", value= "**Commands**", inline=False)
  await goalInput.channel.send(embed=embed)

  
# DELETE SPECIFIC GOAL
async def delete_goal(goalInput):
  userId = goalInput.author.id
  goalToDeleteId = int(goalInput.content.replace('$delete ', '').replace(" ", ""))
  dbEntry = collection.find_one({"userId" : userId})
  totalGoals = dbEntry["totalGoalsNumber"]
  goalArray = dbEntry["goals"]

  if (goalToDeleteId <= 0 or goalToDeleteId > totalGoals):
    await goalInput.channel.send("⚠️ ERROR: Sorry, that goal number doesn't seem to exist")
    return

  goalArray.pop(goalToDeleteId - 1)

  num = 0
  for goal in goalArray:
    num = num + 1
    if (num < goalToDeleteId):
      continue
    else:
      goal["number"] =  goal["number"] - 1
      
  collection.update_one({"userId" : userId}, { "$set": { "goals": goalArray} })
  collection.update_one({"userId" : userId}, { "$set": { "totalGoalsNumber": int(dbEntry["totalGoalsNumber"]) - 1} })

  await my_goals(goalInput)

# VIEW ALL PERSONAL GOALS
async def my_goals(goalInput):
  username = goalInput.author.name
  userId = goalInput.author.id
  
  embed = discord.Embed(title="__View {}'s Goals__".format(username), color= discord.Colour.purple())
  embed.set_footer(text="Type $commands for a list of commands")

  goals = collection.find_one({"userId" : userId})["goals"]

  for goal in goals:
     embed.add_field(name="{}. {}".format(goal["number"], goal["message"]), value= goal["status"], inline=False) 
    
  embed.add_field(name="\u200b", value= "**Commands**", inline=False)
  await goalInput.channel.send(embed=embed)

# ADD NEW GOAL
async def insert_goal_to_db(goalInput):
  userId = goalInput.author.id
  dbEntry = collection.find_one({"userId" : userId})
  message = goalInput.content.replace('$new ', '')
  username = goalInput.author.name
  date = datetime.datetime.now()
  
  #check profanity
  response = requests.get('https://www.purgomalum.com/service/containsprofanity?text={}'
             .format(message))
  json_data = json.loads(response.text)

  if (json_data == True):
    await goalInput.channel.send('⚠️ ERROR: Hmm.. Looks like our bot detected profanity, please try again!')
    return
  
  # check if user exists already
  if (collection.count_documents({"userId" : userId}, limit = 1) == 0):
    print("user doesnt exist")
    goals = [{"number": 1, "message": message, "status": "IN PROGRESS 🕑"}]
    goalToInsert = classDefn.Schema(1,goals,goalInput.author.id,username,date)
    await goalInput.channel.send('⚠️ Note: Your goals are public to the server members')
    collection.insert_one(vars(goalToInsert))
  else:
    print("user exists already")
    newGoalNumber = dbEntry["totalGoalsNumber"] + 1
    if (newGoalNumber > 10):
      await goalInput.channel.send('⚠️ Note: You can have a maximum of 10 goals')
      return
    goalArray = dbEntry["goals"]
    goalArray.append({"number": newGoalNumber, "message": message, "status": "IN PROGRESS 🕑"})
    collection.update_one({"userId" : userId}, { "$set": { "goals": goalArray} })
    collection.update_one({"userId" : userId}, { "$set": { "totalGoalsNumber": newGoalNumber} })       
  #increase list number by one
  collection.update_one({"userId" : userId}, { "$set": { "date": date} })
  await my_goals(goalInput)
  
