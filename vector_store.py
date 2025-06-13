import os
import logging
import pickle
from typing import List, Dict, Any, Optional
import faiss
import numpy as np
from openai import OpenAI

logger = logging.getLogger(__name__)

class VectorStore:
    """FAISS-based vector store for document embeddings"""
    
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "your-api-key-here"))
        self.index = None
        self.documents = []
        self.embeddings_dim = 1536  # OpenAI text-embedding-3-small dimension
        self.index_file = "vector_store.faiss"
        self.docs_file = "documents.pkl"
    
    def get_embedding(self, text: str) -> List[float]:
        """Get embedding for a text using OpenAI API"""
        try:
            response = self.openai_client.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error getting embedding: {e}")
            return [0.0] * self.embeddings_dim
    
    def create_index(self, documents: List[Dict[str, Any]]):
        """Create FAISS index from documents"""
        logger.info(f"Creating vector index for {len(documents)} documents")
        
        # Generate embeddings for all documents
        embeddings = []
        self.documents = documents
        
        for i, doc in enumerate(documents):
            if i % 10 == 0:
                logger.info(f"Processing document {i+1}/{len(documents)}")
            
            embedding = self.get_embedding(doc['text'])
            embeddings.append(embedding)
        
        # Convert to numpy array
        embeddings_array = np.array(embeddings, dtype=np.float32)
        
        # Create FAISS index
        self.index = faiss.IndexFlatL2(self.embeddings_dim)
        self.index.add(embeddings_array)
        
        logger.info(f"Created FAISS index with {self.index.ntotal} vectors")
        
        # Save index and documents
        self.save_index()
    
    def load_index(self) -> bool:
        """Load existing FAISS index and documents"""
        try:
            if os.path.exists(self.index_file) and os.path.exists(self.docs_file):
                self.index = faiss.read_index(self.index_file)
                with open(self.docs_file, 'rb') as f:
                    self.documents = pickle.load(f)
                logger.info(f"Loaded FAISS index with {len(self.documents)} documents")
                return True
        except Exception as e:
            logger.error(f"Error loading index: {e}")
        return False
    
    def save_index(self):
        """Save FAISS index and documents"""
        try:
            if self.index is not None:
                faiss.write_index(self.index, self.index_file)
                with open(self.docs_file, 'wb') as f:
                    pickle.dump(self.documents, f)
                logger.info("Saved FAISS index and documents")
        except Exception as e:
            logger.error(f"Error saving index: {e}")
    
    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar documents"""
        if self.index is None:
            logger.error("Index not loaded")
            return []
        
        try:
            # Get query embedding
            query_embedding = self.get_embedding(query)
            query_vector = np.array([query_embedding], dtype=np.float32)
            
            # Search
            distances, indices = self.index.search(query_vector, k)
            
            # Return results
            results = []
            for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
                if idx < len(self.documents):
                    doc = self.documents[idx].copy()
                    doc['score'] = float(distance)
                    doc['rank'] = i + 1
                    results.append(doc)
            
            logger.debug(f"Found {len(results)} similar documents for query")
            return results
            
        except Exception as e:
            logger.error(f"Error searching: {e}")
            return []
    
    def get_stats(self) -> Dict[str, Any]:
        """Get vector store statistics"""
        return {
            'total_documents': len(self.documents) if self.documents else 0,
            'index_size': self.index.ntotal if self.index else 0,
            'embedding_dimension': self.embeddings_dim,
            'index_loaded': self.index is not None
        }
