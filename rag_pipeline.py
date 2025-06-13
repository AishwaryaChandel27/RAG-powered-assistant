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
        
        # Prepare context from retrieved documents
        context_parts = []
        for i, doc in enumerate(retrieved_docs[:3]):  # Use top 3 documents
            context_parts.append(f"Document {i+1}:")
            context_parts.append(f"Title: {doc['metadata']['title']}")
            context_parts.append(f"Author: {doc['metadata']['username']}")
            context_parts.append(f"Content: {doc['text'][:800]}...")  # Limit content length
            context_parts.append("")
        
        context = "\n".join(context_parts)
        
        # Create prompt
        system_prompt = """You are an AI assistant specialized in answering questions about AI/ML publications and research. 
        You have access to a collection of AI/ML publications and should provide accurate, helpful responses based on the provided context.
        
        Guidelines:
        - Answer based on the provided context from the publications
        - If the context doesn't contain relevant information, say so clearly
        - Provide specific details when available (authors, titles, techniques mentioned)
        - Be concise but informative
        - If asked about specific papers or topics, reference the relevant publications by title and author
        """
        
        user_prompt = f"""Based on the following publications, please answer this question: {query}

Context from relevant publications:
{context}

Please provide a comprehensive answer based on the information available in these publications."""
        
        try:
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return f"I encountered an error while generating a response: {str(e)}. Please check your OpenAI API key and try again."
    
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
