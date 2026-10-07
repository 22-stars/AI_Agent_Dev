from openai import OpenAI # For communicating with the AI model
from dotenv import load_dotenv # Allows to read environment variables from .env file
import os # For accessing environment variables

# Load environment variables from .env file
load_dotenv()

# Create client that communicates with Ollama
client = OpenAI(
  base_url=os.getenv("BASE_URL"),
  api_key=os.getenv("API_KEY")
)

response = client.chat.completions.create(
  model=os.getenv("MODEL"),
  messages=[
    {
      "role": "user",
      "content": "Explain python to a 10 year old?"
    }
  ]
)

# Display the response
print(response.choices[0].message.content)
   