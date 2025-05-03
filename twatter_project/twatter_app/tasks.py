from datetime import datetime
import requests
import google.generativeai as genai
import random

from .keys import GEMINI_API_KEY, NEWSAPI_KEY

from .models import Joke  # ✅ import your Django model

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash-preview-04-17")

def generate_joke(headline: str, persona: str = None) -> str:
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

    if persona is None:
        persona = random.choice(list(prompt_templates.keys()))
    prompt = prompt_templates.get(persona)

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating joke: {e}"

NEWS_API_ENDPOINT = "https://newsapi.org/v2/top-headlines"
PARAMS = {
    "country": "us",
    "pageSize": 100,
    "category": "general",
    "apiKey": NEWSAPI_KEY
}

def fetch_headlines():
    try:
        response = requests.get(NEWS_API_ENDPOINT, params=PARAMS)
        response.raise_for_status()
        data = response.json()

        if data.get("status") != "ok":
            print("News API returned non-ok status")
            return []

        headlines = []
        for article in data["articles"]:
            print("Article:", article)  # Debugging line
            title = article.get("title")
            if not title:
                continue

            # Optional: avoid duplicates
            if Joke.objects.filter(headline=title).exists():
                continue

            joke_text = generate_joke(title)

            # Save to database
            joke_obj = Joke.objects.create(
                headline=title,
                joke=joke_text,
                source=article.get("source", {}).get("name"),
                url=article.get("url"),
                published_at=article.get("publishedAt")
            )

            # Add to response list (for UI)
            headlines.append({
                "title": joke_obj.headline,
                "joke": joke_obj.joke,
                "source": joke_obj.source,
                "url": joke_obj.url,
                "publishedAt": joke_obj.published_at,
                "fetchedAt": joke_obj.fetched_at
            })

            print(f"✅ Saved joke for: {title}")

        return headlines

    except requests.RequestException as e:
        print("Error fetching news:", e)
        return []
