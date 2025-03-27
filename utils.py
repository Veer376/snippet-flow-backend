import numpy as np
import os

embedding_dimentions = int(os.getenv('EMBEDDING_DIMS', 768))

def get_embeddings(text: str) -> np.ndarray:
    # get the embeddings for the text for now we would use the random embeddings
    embedding = np.random.rand(embedding_dimentions)
    return embedding