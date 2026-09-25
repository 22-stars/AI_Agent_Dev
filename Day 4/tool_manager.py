from tools import (
  get_current_time,
  roll_dice,
  generate_password 
)

def execute_tool(user_input):
  text = user_input.lower()

  if "time" in text:
    return get_current_time()
  
  elif "dice" in text:
    return roll_dice()

  elif "password" in text:
    return generate_password()

  else:
    return None

