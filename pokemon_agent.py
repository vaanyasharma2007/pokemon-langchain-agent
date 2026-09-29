import requests

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_ollama import ChatOllama


@tool
def get_pokemon_data(pokemon_name: str) -> dict:
    """
    Get factual information about a Pokemon from PokeAPI.

    Use this tool whenever the user asks about a Pokemon's
    stats, height, weight, types, or abilities.

    The input should be only the Pokemon's name.

    If the Pokemon does not exist, the tool returns an error.
    """

    name = pokemon_name.strip().lower()

    url = f"https://pokeapi.co/api/v2/pokemon/{name}"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 404:
            return {
                "error": f"No Pokemon named '{pokemon_name}' was found."
            }

        response.raise_for_status()

        data = response.json()

        return {
            "name": data["name"],
            "height_m": data["height"] / 10,
            "weight_kg": data["weight"] / 10,
            "types": [
                item["type"]["name"]
                for item in data["types"]
            ],
            "abilities": [
                item["ability"]["name"]
                for item in data["abilities"]
            ],
            "stats": {
                item["stat"]["name"]: item["base_stat"]
                for item in data["stats"]
            }
        }

    except requests.RequestException as error:
        return {
            "error": f"Could not contact PokeAPI: {error}"
        }


model = ChatOllama(
    model="qwen3:4b",
    temperature=0
)


SYSTEM_PROMPT = """
You are a concise and reliable assistant.

You have access to get_pokemon_data.

Rules:
1. Use get_pokemon_data whenever the user asks for factual
   Pokemon information such as stats, height, weight, types,
   or abilities.
2. Never invent Pokemon data.
3. Base Pokemon facts only on information returned by the tool.
4. If the tool returns an error saying the Pokemon does not
   exist, clearly explain that it could not be found.
5. Do not use the Pokemon tool for questions unrelated to
   Pokemon data.
6. Answer the user's original question naturally and concisely.
"""


agent = create_agent(
    model=model,
    tools=[get_pokemon_data],
    system_prompt=SYSTEM_PROMPT
)


def ask(question: str):
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        }
    )

    print("\n" + "=" * 70)
    print("QUESTION:", question)
    print("=" * 70)

    for message in result["messages"]:
        print(f"\n{message.__class__.__name__}:")

        if getattr(message, "content", None):
            print(message.content)

        if getattr(message, "tool_calls", None):
            print("TOOL CALLS:")
            print(message.tool_calls)

    print("\nFINAL ANSWER:")
    print(result["messages"][-1].content)


if __name__ == "__main__":

    questions = [
        "What are the stats of the Pokémon Totodile?",
        "How much does Gyarados weigh, and what types is it?",
        "What abilities does Pikachu have?",
        "What's the height of a Pokémon called Zzzzyxx?",
        "What's your favorite color?"
    ]

    for question in questions:
        ask(question)