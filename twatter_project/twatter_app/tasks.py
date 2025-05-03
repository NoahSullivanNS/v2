import requests
from datetime import datetime

import google.generativeai as genai

# Configure the Gemini API key
genai.configure(api_key="AIzaSyAx0sS0BjK9-p3KNU_U9WBUj0nwNq-JJsU")

# Initialize Gemini model
model = genai.GenerativeModel("gemini-2.5-flash-preview-04-17")

# Function to generate a joke based on a headline
def generate_joke(headline: str, persona: str = "Late Night Host") -> str:
    """
    Generates a joke based on the provided headline and persona using Google Gemini API.

    Parameters:
        headline (str): The news headline to base the joke on.
        persona (str): The persona style for the joke generation.

    Returns:
        str: The generated joke or error message.
    """

    prompt_templates = {
        "Late Night Host": f"You are a late-night talk show host with a sharp wit. Given this real news headline: \"{headline}\", write a fake tweet in your voice, using humor and sarcasm.",
        "Paranoid Conspiracy Uncle": f"You are a paranoid conspiracy uncle who believes that everything is connected to some global agenda. Given this real news headline: \"{headline}\", write a tweet exposing the 'truth' in an absurd, wild way.",
        "Zoomer Shitposter": f"You are a zoomer who lives on meme pages and Twitter. Given this news headline: \"{headline}\", write a chaotic, meme-filled tweet like a shitpost.",
        "AI Bot Who Tries Too Hard": f"You are an AI bot trying to be funny but failing awkwardly. Given this headline: \"{headline}\", write a joke that is overly formal, weird, and totally unfunny.",
        "Political Pundit": f"You are a political pundit who overanalyzes everything. Given this headline: \"{headline}\", write a sarcastic tweet that exaggerates its political implications.",
        "Boomer Dad": f"You are a boomer dad making dad jokes. Given this news headline: \"{headline}\", write a tweet full of puns and classic dad humor.",
        "Optimistic Influencer": f"You are a super positive influencer. Given this headline: \"{headline}\", write an upbeat, emoji-filled tweet turning it into an inspiring moment.",
        "Cynical Old Man": f"You are a grumpy old man who complains about everything. Given this headline: \"{headline}\", write a bitter, sarcastic tweet like you’ve seen it all before.",
        "Overly Dramatic Theatre Actor": f"You are a theatre actor with a flair for the dramatic. Given this headline: \"{headline}\", write a tweet that sounds like a Shakespearean tragedy.",
        "Shakespearean": f"You are William Shakespeare on Twitter. Given this headline: \"{headline}\", write a poetic and absurdly dramatic tweet using Elizabethan language."
    }

    # If no persona is provided, choose one at random
    if persona is None:
        persona = random.choice(list(prompt_templates.keys()))

    prompt = prompt_templates.get(persona, prompt_templates["Late Night Host"])

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error: {e}"

NEWSAPI_KEY = "074b7a5bdd274bb68ab9da5df5574e2e"  # replace with your actual key
NEWS_API_ENDPOINT = "https://newsapi.org/v2/top-headlines"
PARAMS = {
    "country": "us",
    "pageSize": 10,
    "category": "general",
    "apiKey": NEWSAPI_KEY
}

def fetch_headlines():
    try:
        response = requests.get(NEWS_API_ENDPOINT, params=PARAMS)
        response.raise_for_status()
        data = response.json()

        if data.get("status") != "ok":
            print("Failed to fetch news:", data)
            return []

        headlines = []
        for article in data["articles"]:
            headline_text = article.get("title")
            joke = generate_joke(headline_text)  # auto random persona
            headlines.append({
                "title": headline_text,
                "description": article.get("description"),
                "url": article.get("url"),
                "publishedAt": article.get("publishedAt"),
                "source": article.get("source", {}).get("name"),
                "fetchedAt": datetime.utcnow().isoformat(),
                "joke": joke
            })
            print(f"- {headline_text} (Source: {article.get('source', {}).get('name')})")
            print(joke)

        return headlines

    except requests.RequestException as e:
        print("Error fetching news:", e)
        return []
