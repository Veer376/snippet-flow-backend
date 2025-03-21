import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()
embedding_dimentions = os.get('EMBEDDING_DIMS', 100)
def get_embeddings(text: str|None,) -> np.ndarray:
    # get the embeddings for the text for now we would use the random embeddings
    embedding = np.random.rand(embedding_dimentions)
    return embedding