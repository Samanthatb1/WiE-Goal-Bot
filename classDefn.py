import datetime

class Schema:
  totalGoalsNumber = 0
  goals = []
  userId= 0
  username = 0
  date = datetime.datetime.now()

  def __init__(self, totalGoalsNumber, goals, userId, username, date):
    self.totalGoalsNumber = totalGoalsNumber
    self.goals = goals
    self.userId = userId
    self.username = username
    self.date = date
