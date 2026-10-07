from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


def build_tool_descriptions(tools):

    descriptions = ""

    for tool in tools:

        descriptions += f"""
Tool:
{tool.name}

Description:
{tool.description}

----------------------------
"""

    return descriptions

def planner(state, tools):

    tool_descriptions = build_tool_descriptions(tools)

    actions_str = ", ".join(state["actions"]) if state["actions"] else "None"

    observations_str = "\n".join([f"- {o['action']}: {o['observation']}" for o in state["observations"]]) if state["observations"] else "None"

    prompt = f"""
You are an AI Planner.

Your job is to decide the next action OR return FINISH if the request is complete.

User Request:
{state["user_request"]}

Completed Actions:
{actions_str}

Previous Observations:
{observations_str}

Available Tools:
{tool_descriptions}

Rules:

1. Choose only ONE next action.
2. Never repeat an action that has already been completed.
3. Use the observations to decide what is still required.
4. If all tools needed for the user's request are in Completed Actions, return FINISH.
5. Do not select tools that are not related to the user's request.
6. Return ONLY the tool name or FINISH.
7. Do not explain your answer.

Next Action:
"""

    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {
                "role": "system",
                "content": "You are an AI planner."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content.strip().strip(".").strip()

