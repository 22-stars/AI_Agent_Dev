from openai import OpenAI
from dotenv import load_dotenv
from similarity import cosine_similarity
import os

load_dotenv()

client = OpenAI(
    base_url=os.getenv("EMBEDDING_BASE_URL"),
    api_key=os.getenv("API_KEY")
)

def create_embedding(content):
    embedding1 = client.embeddings.create(
    model=os.getenv("EMBEDDING_MODEL"),
    input=content
    ).data[0].embedding
    return embedding1





