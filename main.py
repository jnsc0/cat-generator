import os
import openai
import streamlit as st
import time
import requests
import json
from dotenv import find_dotenv, load_dotenv


load_dotenv()

assistant_id = os.environ.get("ASSISTANT_ID")
client = openai.OpenAI()
CAT_API_KEY = os.environ.get("CAT_API_KEY")
gpt_model = "gpt-3.5-turbo-16k"

# Mapping breed name : breed id
BREED_ID_MAP = {
    "abyssinian": "abys",
    "aegean": "aege",
    "american bobtail": "abob",
    "american curl": "acur",
    "american shorthair": "asho",
    "american wirehair": "awir",
    "arabian mau": "amau",
    "australian mist": "amis",
    "balinese": "bali",
    "bambino": "bamb",
    "bengal": "beng",
    "birman": "birm",
    "bombay": "bomb",
    "british longhair": "bslo",
    "british shorthair": "bsho",
    "burmese": "bure",
    "burmilla": "buri",
    "california spangled": "cspa",
    "chantilly-tiffany": "ctif",
    "chartreux": "char",
    "chausie": "chau",
    "cheetoh": "chee",
    "colorpoint shorthair": "csho",
    "cornish rex": "crex",
    "cymric": "cymr",
    "cyprus": "cypr",
    "devon rex": "drex",
    "donskoy": "dons",
    "dragon li": "lihu",
    "egyptian mau": "emau",
    "european burmese": "ebur",
    "exotic shorthair": "esho",
    "havana brown": "hbro",
    "himalayan": "hima",
    "japanese bobtail": "jbob",
    "javanese": "java",
    "khao manee": "khao",
    "korat": "kora",
    "kurilian": "kuri",
    "laperm": "lape",
    "maine coon": "mcoo",
    "malayan": "mala",
    "manx": "manx",
    "munchkin": "munc",
    "nebelung": "nebe",
    "norwegian forest cat": "norw",
    "ocicat": "ocic",
    "oriental": "orie",
    "persian": "pers",
    "pixie-bob": "pixi",
    "ragamuffin": "raga",
    "ragdoll": "ragd",
    "russian blue": "rblu",
    "savannah": "sava",
    "scottish fold": "sfol",
    "selkirk rex": "srex",
    "siamese": "siam",
    "siberian": "sibe",
    "singapura": "sing",
    "snowshoe": "snow",
    "somali": "soma",
    "sphynx": "sphy",
    "tonkinese": "tonk",
    "toyger": "toyg",
    "turkish angora": "tang",
    "turkish van": "tvan",
    "york chocolate": "ycho",
}


def get_cat(breed_id=None):
    if breed_id:
        url = f"https://api.thecatapi.com/v1/images/search?breed_ids={breed_id}&limit=1&api_key={CAT_API_KEY}"
    else:
        url = f"https://api.thecatapi.com/v1/images/search?size=med&mime_types=jpg&format=json&has_breeds=true&order=RANDOM&page=0&limit=1&api_key={CAT_API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            cats_json = response.json()
            if cats_json and "breeds" in cats_json[0]:
                cat_data = cats_json[0]
                cat_url = cat_data["url"]
                cat_breed = cat_data["breeds"][0]["name"] if cat_data["breeds"] else "Unknown"
            elif cats_json:
                cat_data = cats_json[0]
                cat_url = cat_data["url"]
                cat_breed = "Random Cat"
            else:
                return "Unknown", None
            return cat_breed, cat_url
        else:
            return "Unknown", None
    except requests.exceptions.RequestException as e:
        print("Error occurred during API Request", e)
        return "Unknown", None




if "start_chat" not in st.session_state:
    st.session_state.start_chat = False
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

st.set_page_config(page_title="CatGPT", page_icon=":speech_balloon:")


if st.sidebar.button("Start Chat"):
    st.session_state.start_chat = True
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id

st.title("Generate Random Cats")
st.write("Cats meow meow")

if st.button("Exit Chat"):
    st.session_state.messages = []  # Clear the chat history
    st.session_state.start_chat = False  # Reset the chat state
    st.session_state.thread_id = None

if st.session_state.start_chat:
    if "openai_model" not in st.session_state:
        st.session_state.openai_model = gpt_model
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What cat image would you like?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        selected_breed = next((breed_id for breed_name, breed_id in BREED_ID_MAP.items() if breed_name in prompt.lower()), None)
        if selected_breed:
            cat_breed, cat_url = get_cat(selected_breed)
            # st.write(f"Cat Breed: {cat_breed}")
            # if cat_url:
            #     st.image(cat_url, caption=f"{cat_breed} Cat Image")
            # else:
            #     st.write("No image available for the specified breed.")
        else:
            cat_breed, cat_url = get_cat()
            # st.write(f"Cat Breed: {cat_breed}")
            # if cat_url:
            #     st.image(cat_url, caption="Random Cat Image")
            # else:
            #     st.write("No random cat image available.")

        ##user message
        client.beta.threads.messages.create(
                thread_id=st.session_state.thread_id,
                role="user",
                # content=prompt
                content=f"Display {cat_url} "
            )
        
        ##create thread
        run = client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=assistant_id,
            instructions=f"You are the best at displaying ONLY {cat_url}. \nPlease return THIS {cat_url} image.\nDISPLAY ONLY: {cat_url}. \n ONLY DISPLAY THE IMAGE FROM THE Cat Image URL: {cat_url}."
        )

        while run.status != 'completed':
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(
                thread_id=st.session_state.thread_id,
                run_id=run.id
            )
        messages = client.beta.threads.messages.list(
            thread_id=st.session_state.thread_id
        )

        # Process and display assistant messages
        assistant_messages_for_run = [
            message for message in messages 
            if message.run_id == run.id and message.role == "assistant"
        ]
        for message in assistant_messages_for_run:
            st.session_state.messages.append({"role": "assistant", "content": message.content[0].text.value})
            with st.chat_message("assistant"):
                st.markdown(message.content[0].text.value)                

else:
    st.write("Click 'Start Chat' to begin.")
