import faiss
import numpy as np

class VectorSearchService:
    def __init__(self,vector_size:int):
        self.index=faiss.IndexFlatL2(vector_size)

    def add_vector(self,vectors:np.ndarray):
        self.index.add(vectors)

    def search(self,query_vector:np.ndarray,top_k=5):

        distances,indices=self.index.search(query_vector,top_k)
        return indices,distances
