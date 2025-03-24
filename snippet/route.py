from fastapi import APIRouter, HTTPException
from schema import Interaction, User, Snippet
from database import SessionLocal
import model
from kafka_app.producer import produce_message

snippet_router = APIRouter(prefix='/snippet')

@snippet_router.post('/rating', status_code=201)
def rate_snippet(interaction: Interaction):
    """
    Store user snippet interaction (like, dislike, neutral).
    """
    user_id = interaction.user_id
    snippet_id = interaction.snippet_id
    rating = interaction.rating
    try:
        with SessionLocal() as db:
            db_interaction = model.UserSnippetInteraction(user_id=user_id, snippet_id=snippet_id, rating=rating)
            db.add(db_interaction)
            db.commit()
            return {'message': 'Rating saved'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"There was an error while saving the rating: {str(e)}")


@snippet_router.get('/recommendations')
def get_recommendations(user: User):
    """
    Fetch recommendations for the user using OpenSearch and pdvector.
    """
    try:
        # Placeholder for recommendation logic
        recommendations = []  # Fetch from OpenSearch or vector-based model
        return {'message': 'Recommendations fetched', 'recommendations': recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching recommendations: {str(e)}")


@snippet_router.post('/save', status_code=201)
def save_snippet(snippet: Snippet):
    """
    Save a new snippet and produce a Kafka message for processing.
    """
    try:
        with SessionLocal() as db:
            db_snippet = model.Snippet(text=snippet.text, author=snippet.author)
            db.add(db_snippet)
            db.commit()
            db.refresh(db_snippet)

            # Produce the message to Kafka
            produce_message("new-snippet", db_snippet.id, db_snippet.text)
            return {'message': 'Snippet has been saved.', 'id': db_snippet.id}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"There was an error while saving the snippet: {str(e)}")
