from openai.resources.beta.threads import messages
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
  base_url = os.getenv("BASE_URL"),
  api_key = os.getenv("API_KEY")

)

# Printing the title
print("=" * 20)
print("AI ASSISTANT")
print("=" * 20) 

# Storing the conversation history
msgs = []

while True:
  user_input = input("\nYou: ")
  
  # Breaking the loop if user enters exit or quit
  if user_input.lower() == 'exit' or user_input.lower() == 'quit':
    print("\nGood Bye!")
    break

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
  print("\n----------Conversation history-------------")
  for msg in msgs:
    print(f"{msg['role'].title()}: {msg['content']}\n")
  print("---------------------")