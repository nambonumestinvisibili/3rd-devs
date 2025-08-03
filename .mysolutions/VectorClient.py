from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
from globals import openapi_api_key

EMBEDDING_MODEL = "text-embedding-3-small"
VECTOR_MODEL = 'openai-embedding'

class VectorClient:
  def __init__(self, collection_name):
    self.collection = collection_name
    self.openai_client = OpenAI(api_key=openapi_api_key)
    self.vector_client = QdrantClient(host="localhost", port=6333)

  def create_embedding(self, text):
    response = self.openai_client.embeddings.create(
      input=text,
      model=EMBEDDING_MODEL
    )
    return response.data[0].embedding

  def search(self, query_vector, using=None):
    response = self.vector_client.query_points(
      collection_name=self.collection,
      query=query_vector,
      using=VECTOR_MODEL
    )
    return response

  def upsert(self, point_id, text, payload=None):
    """
    Upserts a vector into the collection.
    :param point_id: Unique identifier for the point.
    :param vector: The embedding vector.
    :param payload: Optional metadata dictionary.
    """
    point = PointStruct(
      id=point_id, 
      vector=self.create_embedding(text), 
      payload={
        text: text,
        **payload
      })
    self.vector_client.upsert(
      collection_name=self.collection,
      points=[point]
    )

  def upsert_many(self, points):
    """
    Upserts multiple vectors into the collection.
    :param points: List of dicts, each with keys 'id', 'vector', and optional 'payload'.
    Example:
      [
      {'id': 1, 'text': 'text', 'payload': {'meta': 'data'}},
      {'id': 2, 'text': 'text'}
      ]
    """
    point_structs = [
      PointStruct(
        id=str(point['id']), 
        vector={VECTOR_MODEL: self.create_embedding(point['text'])},
        payload=point.get('payload'))
      for point in points
    ]

    print(point_structs)

    self.vector_client.upsert(
      collection_name=self.collection,
      points=point_structs
    )
