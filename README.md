# LangChain PokeAPI Agent

This project implements a simple agentic AI workflow using LangChain,
Ollama, and the local `qwen3:4b` model.

The agent decides when external Pokemon data is needed, calls a Python
tool that queries PokeAPI, and then uses the returned data to answer
the original question in natural language.

## Setup

1. Install Ollama
2. Pull the model:

   ollama pull qwen3:4b

3. Create and activate a Python virtual environment
4. Install dependencies:

   pip install -r requirements.txt

5. Run:

   python pokemon_agent.py

## Tool

The agent has one tool: `get_pokemon_data`.

It retrieves:

- height
- weight
- types
- abilities
- stats

The PokeAPI response is reduced to only the useful fields before being
returned to the model, which helps reduce context usage for the small
local model.

## Error Handling

If a Pokemon does not exist, the tool returns an explicit error instead
of allowing the model to invent an answer.

For example, the query about `Zzzzyxx` correctly reports that the Pokemon
does not exist.

## Agent Behavior

The agent uses the Pokemon tool only when factual Pokemon data is needed.

For unrelated questions, such as asking for a favorite color, the model
answers directly without calling the tool.

## Observations

A key challenge was reliable tool calling with a small local model.
Clear tool descriptions and a concise system prompt were important for
getting consistent behavior.