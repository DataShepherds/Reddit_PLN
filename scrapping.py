#!pip install praw pandas nltk spacy pyspellchecker
import praw

reddit = praw.Reddit(
    client_id="client_id",
    client_secret="client_secret",
    user_agent="PLN"
)

import json
from tqdm import tqdm

SUBREDDITS = ["nba", "deeplearning", "nasa", "movies", "politics", "science"]
MAX_THREADS_PER_SUBREDDIT = 20
COMMENTS_PER_THREAD = 50

def scrape_reddit():
    for subreddit_name in SUBREDDITS:
        subreddit = reddit.subreddit(subreddit_name)
        threads_data = []
        
        # Buscar hilos populares (ajustar parámetros según necesidad)
        for thread in tqdm(subreddit.top(limit=MAX_THREADS_PER_SUBREDDIT), desc=f"Extrayendo de r/{subreddit_name}"):
            if thread.over_18:  # Saltar contenido NSFW
                continue
                
            comments = []
            thread.comments.replace_more(limit=0)  # Limitar comentarios anidados
            for comment in thread.comments[:COMMENTS_PER_THREAD]:
                comments.append({
                    "user": str(comment.author),
                    "comment": comment.body,
                    "score": comment.score,
                    "date": comment.created_utc
                })
            
            threads_data.append({
                "flair": thread.link_flair_text,
                "title": thread.title,
                "author": str(thread.author),
                "date": thread.created_utc,
                "score": thread.score,
                "description": thread.selftext,
                "comments": comments
            })
        
        # Guardar en JSON
        with open(f"subreddit_{subreddit_name}.json", "w", encoding="utf-8") as f:
            json.dump(threads_data, f, indent=4, ensure_ascii=False)

scrape_reddit()