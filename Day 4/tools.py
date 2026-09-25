from datetime import datetime 
import random
import secrets
import string

def get_current_time():
  return datetime.now().strftime('%d-%m-%Y %I:%M:%S %p')

def roll_dice():
  return random.randint(1,6)

def generate_password(length = 12):
  characters = string.ascii_letters + string.digits + string.punctuation
  password = ""
  for i in range(length):
    password += secrets.choice(characters)
  return password

  

