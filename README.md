# Cat Generator 

This repository contains a simple cat generator application that utilizes OpenAI's GPT-3.5 model along with TheCatAPI to generate and display random cat images based on user prompts.

## Getting Started

To run the cat generator application, follow these steps:

1. Clone this repository to your local machine:

   ```bash
   
   git clone <github.com/jnsc0/cat-generator>
   ```

2. Install the required dependencies. You can use pip to install them:

   ```bash
   
   pip install -r requirements.txt
   ```

3. Set up your environment variables. You need to have access to TheCatAPI and an OpenAI assistant. You can obtain API keys for TheCatAPI from their [official website](https://thecatapi.com/) and for OpenAI from the [OpenAI website](https://openai.com/). Once you have your keys, create a `.env` file in the root directory of the project and add the following:

   ```dotenv
   
   ASSISTANT_ID=<your-openai-assistant-id>
   CAT_API_KEY=<your-catapi-key>
   OPENAI_API_KEY=<your-openai-api-key>
   ```

4. Run the Streamlit application:

   ```bash
   streamlit run app.py
   ```

## Usage

Once the application is running, you can interact with it using the provided user interface. Here are the main functionalities:

- Click "Start Chat" to initiate a chat session with the OpenAI assistant.
- Enter your prompt/query in the chat box to request a specific cat image. For example, you can type "Show me a Siamese cat" to get an image of a Siamese cat.
- The application will fetch a random cat image from TheCatAPI based on your prompt and display it.
- You can exit the chat session at any time by clicking "Exit Chat".

---
This project was created with ❤️ by jnsc0.
