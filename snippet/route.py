# there will be routes of like, dislike , and then getting the recommedations.

from fastapi import APIRouter
from schema import Interaction, User
from database import SessionLocal
import schema
import model

snippet_router = APIRouter(prefix='/snippet')

@snippet_router.post('/rating')
def rate_snippet(interation: Interaction):
    # rating 1 -> like, -1 -> dislike, 0 -> neutral
    user_id = interation.user_id
    snippet_id = interation.snippet_id
    rating = interation.rating
    try:
        db = SessionLocal()
        db_interaction = model.UserSnippetInteraction(user_id=user_id, snippet_id=snippet_id, rating=rating)
        db.add(db_interaction)
        db.commit()
        return {'message' : 'Rating saved'}
    except Exception as e:
        return {'message' : 'There was an error while saving the rating'}


@snippet_router.get('/recommendations')
def get_recommendations(user: schema.User):
    # get the recommendations for the user using opensearch
    # for now we would like to use the pdvector.
    return {'message': 'Recommendations fetched'}

@snippet_router.post('/save')
def save_snippet(snippet : schema.Snippet):
    # user will send us the snippet.
    db_snippet = model.Snippet(text=snippet.text, author=snippet.author)
    try:
        db = SessionLocal()
        db.add(db_snippet)
        db.commit()
        return {'message': 'Sit back and relax the Snippet has been saved.'}
    except Exception as e:
        return {'message': 'There was an error while saving the snippet'}