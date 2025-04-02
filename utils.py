import numpy as np
import os
import boto3
import json
from botocore.exceptions import ClientError

embedding_dimentions = int(os.getenv('EMBEDDING_DIMS', 1024))

def get_embeddings(text: str) -> np.ndarray:
    # get the embeddings for the text for now we would use the random embeddings
    embedding = np.random.rand(embedding_dimentions)
    return embedding

def get_embeddings_bedrock(text: str) -> list:
    """Get the embeddings for a given text using Amazon Bedrock."""

    brt = boto3.client("bedrock-runtime")

    # Set the model ID, e.g., Amazon Titan Text G1 - Express.
    model_id = "amazon.titan-embed-text-v2:0"

    # Format the request payload using the model's native structure.
    native_request = {
        "inputText": text,
    }

    request = json.dumps(native_request)

    try:
        response = brt.invoke_model(modelId=model_id, body=request)

    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        exit(1)

    model_response = json.loads(response["body"].read())

    return print(model_response["embedding"])




