from locust import HttpUser, task, between
import numpy as np


class SnippetFlowUser(HttpUser):
    texts = [
        "The only way to do great work is to love what you do.",
        "Life is what happens when you're busy making other plans.",
        "The future belongs to those who believe in the beauty of their dreams.",
        "It is during our darkest moments that we must focus to see the light.",
        "Whoever is happy will make others happy too.",
        "You will face many defeats in life, but never let yourself be defeated.",
        "In the end, it's not the years in your life that count. It's the life in your years.",
        "Never let the fear of striking out keep you from playing the game.",
        "Life is really simple, but we insist on making it complicated.",
        "The purpose of our lives is to be happy."
    ]
    wait_time = between(1, 3)  # Simulate a user waiting 1-3 seconds between tasks

    @task(5)
    def publish_snippet(self):
        payload = {
            "text": str(np.random.choice(self.texts)),
            "author": "Locust Tester"
        }
        self.client.post("/snippet/publish", json=payload)

    @task(2)
    def rate_snippet(self):
        payload = {
            "user_id": int(np.random.randint(1, 20)),
            "snippet_id": int(np.random.randint(1, 50)),
            "rating": int(np.random.choice([-1, 1]))
        }
        self.client.post("/snippet/rating", json=payload)

    @task(3)
    def get_recommendations(self):
        # Replace with the actual payload if needed
        payload = {
            "user_id": int(np.random.randint(1, 20)),
            "email": "test@example.com"
        }
        self.client.post("/snippet/get", json=payload)
    