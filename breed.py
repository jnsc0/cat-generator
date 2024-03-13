import requests
import json

api_url = "https://api.thecatapi.com/v1/breeds"

# Fetch data from the API
response = requests.get(api_url)
breeds_data = response.json()

# Extract "name" and "id" and create the desired format
BREED_ID_MAP = {breed["name"].lower(): breed["id"] for breed in breeds_data}

# Print the result
print("BREED_ID_MAP = {")
for name, breed_id in BREED_ID_MAP.items():
    print(f'    "{name}": "{breed_id}",')
print("}")
