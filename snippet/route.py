from fastapi import APIRouter, HTTPException
from schema import Interaction, User, Snippet
from database import SessionLocal
import model
from kafka_app.producer import produce_message
from utils import get_embeddings
from sqlalchemy import text
import numpy as np
import ast

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
            return {'message': f'Rating saved for user {user_id} on snippet {snippet_id}'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"There was an error while saving the rating: {str(e)}")

@snippet_router.get('/get', response_model=list)
def get_recommendations(user: User):
    """
    Fetch recommendations for the user using OpenSearch and pdvector.
    """
    # Here it can be think as the caveat that the server will send the snippets for any user that is not the registered user, one way off-course is to check the user id but for now we are assuming that the user will have the id only if registered.
    try:
        db = SessionLocal()
        embeddings_cursor = db.execute(text(f"SELECT embedding FROM snippet_embedding WHERE snippet_id IN (SELECT snippet_id FROM usi WHERE user_id = {user.id} AND rating = 1)"))
        embeddings = [ast.literal_eval(row.embedding) for row in embeddings_cursor]
        
        if not embeddings: # return the random snippets if no embeddings are found
            cursor = db.execute(text(f"SELECT s.text, s.author FROM snippet s INNER JOIN snippet_embedding se ON s.id = se.snippet_id ORDER BY RANDOM() LIMIT 10"))
            return [{'text': row.text, 'author':row.author} for row in cursor]
        
        embedding = np.mean(embeddings, axis=0)

        embedding_vector_format = "[" + ",".join(str(x) for x in embedding) + "]"

        recommedations_cursor = db.execute(text(f"SELECT s.text, s.author FROM snippet s INNER JOIN snippet_embedding se ON s.id = se.snippet_id WHERE se.snippet_id NOT IN (SELECT snippet_id FROM usi WHERE user_id = {user.id}) ORDER BY se.embedding <-> '{embedding_vector_format}' LIMIT 10"))

        recommendations = [{'text': row.text, 'author': row.author} for row in recommedations_cursor]
        return recommendations
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching recommendations: {str(e)}")

@snippet_router.post('/publish', status_code=201)
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
            data = {
                'id': db_snippet.id,
                'text': db_snippet.text,
                'author' : db_snippet.author
            }
            produce_message("new-snippet", value=data)

            return {'message': 'Snippet has been saved.', 'id': db_snippet.id}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"There was an error while saving the snippet: {str(e)}")

@snippet_router.post('/consume')
def snippet_consume(snippet: Snippet):
    # format of snippet:
    """ 
    Request body should be in the following format:
    {
        "id": 1,
        "text": "this is the quote you will receive from the kafka consumer",
        "author": "author of the quote"
    }
    """
    try:
        embedding = get_embeddings(snippet.text) # embedding is of type np.ndarray
        db = SessionLocal()
        snippet_embedding = model.SnippetEmbedding(snippet_id=snippet.id, embedding=embedding.tolist())
        db.add(snippet_embedding)
        db.commit()
        db.refresh(snippet_embedding)
        return {'message': 'Snippet has been consumed.', 'id': snippet.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"There was an error while consuming the snippet: {str(e)}")

        