import logging
import re
from typing import List, Dict, Any
from models import Publication
from app import db

logger = logging.getLogger(__name__)

class SimpleTextSearch:
    """Simple text-based search without embeddings for initial functionality"""
    
    def __init__(self):
        self.publications = []
        self.is_initialized = False
    
    def initialize(self):
        """Initialize with publications from database"""
        try:
            self.publications = db.session.query(Publication).all()
            self.is_initialized = True
            logger.info(f"Initialized simple search with {len(self.publications)} publications")
        except Exception as e:
            logger.error(f"Error initializing simple search: {e}")
            self.is_initialized = False
    
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Simple text-based search using keyword matching"""
        if not self.is_initialized:
            return []
        
        query_words = query.lower().split()
        scored_docs = []
        
        for pub in self.publications:
            # Create searchable text
            searchable_text = f"{pub.title} {pub.description}".lower()
            
            # Calculate simple relevance score
            score = 0
            for word in query_words:
                if len(word) > 2:  # Ignore very short words
                    score += searchable_text.count(word)
            
            if score > 0:
                scored_docs.append({
                    'id': pub.id,
                    'text': f"Title: {pub.title}\n\nAuthor: {pub.username}\n\nDescription: {pub.description[:1000]}...",
                    'score': score,
                    'metadata': {
                        'title': pub.title,
                        'username': pub.username,
                        'license': pub.license or '',
                        'pub_id': pub.id
                    }
                })
        
        # Sort by relevance score
        scored_docs.sort(key=lambda x: x['score'], reverse=True)
        
        # Add rank
        for i, doc in enumerate(scored_docs[:top_k]):
            doc['rank'] = i + 1
        
        logger.debug(f"Found {len(scored_docs[:top_k])} relevant documents for query")
        return scored_docs[:top_k]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get search statistics"""
        return {
            'total_documents': len(self.publications),
            'search_method': 'Simple Text Search',
            'initialized': self.is_initialized
        }

# Global simple search instance
simple_search = SimpleTextSearch()