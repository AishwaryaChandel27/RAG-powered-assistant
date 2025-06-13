import os
import logging
import time
from typing import List, Dict, Any, Optional
from openai import OpenAI
from simple_search import simple_search
from data_processor import PublicationProcessor

logger = logging.getLogger(__name__)

class RAGPipeline:
    """RAG (Retrieval-Augmented Generation) pipeline for question answering"""
    
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "your-api-key-here"))
        self.search_engine = simple_search
        self.processor = PublicationProcessor()
        self.is_initialized = False
    
    def initialize(self):
        """Initialize the RAG pipeline"""
        logger.info("Initializing RAG pipeline...")
        
        # Initialize data first
        publications = self.processor.get_all_publications()
        if not publications:
            logger.info("No publications found, loading from JSON...")
            from data_processor import initialize_data
            initialize_data()
        
        # Initialize simple search
        self.search_engine.initialize()
        self.is_initialized = self.search_engine.is_initialized
        
        if self.is_initialized:
            logger.info("RAG pipeline initialized successfully")
        else:
            logger.error("Failed to initialize RAG pipeline")
    
    def retrieve_documents(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve relevant documents for a query"""
        if not self.is_initialized:
            logger.error("RAG pipeline not initialized")
            return []
        
        return self.search_engine.search(query, top_k=top_k)
    
    def generate_response(self, query: str, retrieved_docs: List[Dict[str, Any]]) -> str:
        """Generate response using retrieved documents"""
        if not retrieved_docs:
            return "I couldn't find any relevant information to answer your question. Please try rephrasing your query or asking about AI/ML publications, research, or related topics."
        
        # Since OpenAI API is not available, create a comprehensive response from the retrieved documents
        response_parts = []
        response_parts.append(f"Based on the AI/ML publications in our database, here's what I found regarding your question: '{query}'")
        response_parts.append("")
        
        for i, doc in enumerate(retrieved_docs[:3]):  # Use top 3 documents
            response_parts.append(f"**Publication {i+1}: {doc['metadata']['title']}**")
            response_parts.append(f"Author: {doc['metadata']['username']}")
            if doc['metadata']['license']:
                response_parts.append(f"License: {doc['metadata']['license']}")
            
            # Extract key information from the document text
            doc_text = doc['text']
            if 'Description:' in doc_text:
                description_part = doc_text.split('Description:')[1][:500]
                response_parts.append(f"Summary: {description_part.strip()}...")
            else:
                response_parts.append(f"Content: {doc_text[:400]}...")
            
            response_parts.append("")
        
        response_parts.append("---")
        response_parts.append(f"Found {len(retrieved_docs)} relevant publications. The above shows the top {min(3, len(retrieved_docs))} most relevant results.")
        
        if len(retrieved_docs) > 3:
            response_parts.append("")
            response_parts.append("Additional relevant publications:")
            for doc in retrieved_docs[3:5]:  # Show 2 more titles
                response_parts.append(f"- {doc['metadata']['title']} by {doc['metadata']['username']}")
        
        return "\n".join(response_parts)
    
    def answer_question(self, query: str) -> Dict[str, Any]:
        """Complete RAG pipeline: retrieve and generate answer"""
        start_time = time.time()
        
        if not self.is_initialized:
            return {
                'query': query,
                'answer': "The system is not properly initialized. Please check the setup and try again.",
                'retrieved_docs': [],
                'response_time': 0,
                'error': 'System not initialized'
            }
        
        # Retrieve relevant documents
        retrieved_docs = self.retrieve_documents(query)
        
        # Generate response
        answer = self.generate_response(query, retrieved_docs)
        
        response_time = time.time() - start_time
        
        return {
            'query': query,
            'answer': answer,
            'retrieved_docs': retrieved_docs,
            'response_time': response_time,
            'num_retrieved': len(retrieved_docs)
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get system status and statistics"""
        search_stats = self.search_engine.get_stats()
        
        return {
            'initialized': self.is_initialized,
            'vector_store_stats': search_stats,
            'openai_configured': bool(os.environ.get("OPENAI_API_KEY"))
        }

# Global RAG pipeline instance
rag_pipeline = RAGPipeline()
