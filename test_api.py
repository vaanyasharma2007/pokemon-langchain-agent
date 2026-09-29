import requests

pokemon = "pikachu"

url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"
response = requests.get(url)

print("Status code:", response.status_code)

data = response.json()

print("Name:", data["name"])
print("Height:", data["height"])
print("Weight:", data["weight"])

print("Types:")
for item in data["types"]:
    print("-", item["type"]["name"])

print("Abilities:")
for item in data["abilities"]:
    print("-", item["ability"]["name"])