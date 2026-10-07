from openai import OpenAI
from dotenv import load_dotenv
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools import (
  get_current_time, roll_dice, generate_password
)
from tool_manager import execute_tool

load_dotenv()

client = OpenAI(
  base_url = os.getenv("BASE_URL"),
  api_key = os.getenv("API_KEY")

)

# Printing the title
print("=" * 20)
print("AI ASSISTANT")
print("=" * 20) 

roles = {
    "1": "You are a friendly school teacher. Explain every concept using simple language and real-life examples.",

    "2": "You are a senior Python developer. Explain programming concepts clearly and always include Python examples.",

    "3": "You are an experienced travel guide. Recommend places, food, transportation and travel tips.",

    "4": "You are a motivational coach. Encourage the user and give practical advice with a positive attitude.",

    "5": "You are a professional interviewer. Ask one interview question at a time and provide feedback after each answer."
}


print("\nChoose Your Assistant\n")

print("1. Teacher")
print("2. Python Expert")
print("3. Travel Guide")
print("4. Motivational Coach")
print("5. Interviewer")


choice = input("\nEnter your choice or Press enter for default : ").strip()
default_role = "You are a helpful polite, and versatile AI assistant"

system_prompt = roles.get(choice, default_role)

if choice not in roles:
  print("\nUsing standart AI assistant")

# Storing the conversation history
msgs = [
  {
    "role": "system",
    "content": system_prompt
  }
]

while True:
  user_input = input("\nYou: ").strip()

  if not user_input:
    continue
  
  # Breaking the loop if user enters exit or quit
  if user_input.lower() in ['exit' , 'quit']:
    print("\nGood Bye!")
    break

  #  Checking if the user wants to use a tool
  tool_result = execute_tool(user_input)

  if tool_result:
    print(f"\nAI: {tool_result}")
    continue

# Saving user's message
  msgs.append(
    {
       "role" : "user",
       "content" : user_input
     }
  ) 

  response = client.chat.completions.create(
   model = os.getenv("MODEL"),
   messages=msgs
  )

# Saving assistant's message
  assistant_response = response.choices[0].message.content
  print("\nAssistant: ",assistant_response)
  msgs.append(
    {
      "role" : "assistant",
      "content" : assistant_response
    }
  )
# For debugging
  # print("\n----------Conversation history-------------")
  # for msg in msgs:
  #   print(f"{msg['role'].title()}: {msg['content']}\n")
  # print("---------------------")