# there will be routes of like, dislike , and then getting the recommedations.

from fastapi import Router
from schema import Interaction, User

snippet_router = Router(prefix='/snippet')

@snippet_router.post('/rating')
def rate_snippet(interation: Interaction):
    # set the interaction rating to 1
    return {'message': 'Snippet rated'}

@snippet_router.get('/recommendations')
def get_recommendations(user: User):
    # get the recommendations for the user using opensearch
    # for now we would like to use the pdvector.
    return {'message': 'Recommendations fetched'}