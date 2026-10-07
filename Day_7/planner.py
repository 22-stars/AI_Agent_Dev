from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(base_url=os.getenv("BASE_URL"),
                api_key=os.getenv("API_KEY"))

def choose_tool(user_request):
  planner_prompt = f"""
  you are an AI planner.
  available tools:
  1. get_current_time
     use when the user ask for the current date or time.
  2. get_weather
     use when the user ask for the weather of a specific location.
  if no tool is required, return:
    none  
  Return only the tool name .
  User Request {user_request}"""

  response = client.chat.completions.create(
    model = os.getenv("MODEL"),
    messages = [
      {"role": "user", "content": planner_prompt}
    ]
  )
  return response.choices[0].message.content  