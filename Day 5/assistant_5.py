from openai import OpenAI
from dotenv import load_dotenv
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools import (
  get_current_time, roll_dice, generate_password, read_txt_file
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

  text = user_input.lower()

  if text.startswith("exit") or text.startswith("quit"):
    print("\nGood Bye!")
    break

  if text.startswith("summarize "):
    filename = user_input[10:].strip()
    file_content = read_txt_file("../Data/"+filename)

    prompt = f"""
    Summarize the following text in 3-4 lines:

    Document : {file_content}
    """

    response = client.chat.completions.create(
      model = os.getenv("MODEL"),
      messages = [
        {
          "role" : "system",
          "content" : "You are a helpful assistant"
        },
        {
          "role" : "user",
          "content" : prompt
        }
      ]
    )

    file_summary = response.choices[0].message.content
    print("\nAssistant:", file_summary)
    continue

  if text.startswith("explain "):
    filename = user_input[8:].strip()
    file_content = read_txt_file("../Data/"+filename)

    prompt = f"""
    Explain the following document in simple terms:

    Document : {file_content}
    """

    response = client.chat.completions.create(
      model = os.getenv("MODEL"),
      messages = [
        {
          "role" : "system",
          "content" : "You are a helpful assistant"
        },
        {
          "role" : "user",
          "content" : prompt
        }
      ]
    )

    file_explanation = response.choices[0].message.content
    print("\nAssistant:", file_explanation)
    continue

  if text.startswith("read "):
    filename = user_input[5:].strip()
    file_content = read_txt_file("Data/"+filename)

    prompt = f"""
    You are now given the content of a document. Please acknowledge that
    you have read it and are ready to answer questions about it. If there
    is an error reading the file, point it out.

    Document content:

    {file_content}
    """

    response = client.chat.completions.create(
      model = os.getenv("MODEL"),
      messages = [
        {
          "role" : "system",
          "content" : "You are a helpful assistant"
        },
        {
          "role" : "user",
          "content" : prompt
        }
      ]
    )

    file_knowledge = response.choices[0].message.content
    print("\nAssistant:", file_knowledge)
    continue

  # Checking if the user wants to use a tool
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