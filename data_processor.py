import json
import logging
import re
from typing import List, Dict, Any
from app import app, db
from models import Publication

logger = logging.getLogger(__name__)

class PublicationProcessor:
    """Processes publication data for RAG system"""
    
    def __init__(self):
        self.publications = []
    
    def load_publications_from_json(self, json_file_path: str) -> List[Dict[str, Any]]:
        """Load publications from the provided JSON file"""
        try:
            with open(json_file_path, 'r', encoding='utf-8') as file:
                publications = json.load(file)
            
            logger.info(f"Loaded {len(publications)} publications from {json_file_path}")
            return publications
        except Exception as e:
            logger.error(f"Error loading publications from JSON: {e}")
            return []
    
    def clean_description(self, description: str) -> str:
        """Clean and format publication description"""
        if not description:
            return ""
        
        # Remove image references and dividers
        cleaned = re.sub(r'!\[.*?\]\(.*?\)', '', description)
        cleaned = re.sub(r'--DIVIDER--', '\n\n', cleaned)
        
        # Remove markdown formatting
        cleaned = re.sub(r'\*\*(.*?)\*\*', r'\1', cleaned)  # Bold
        cleaned = re.sub(r'\*(.*?)\*', r'\1', cleaned)      # Italic
        cleaned = re.sub(r'`(.*?)`', r'\1', cleaned)        # Code
        cleaned = re.sub(r'#+ ', '', cleaned)               # Headers
        
        # Remove YouTube embeds
        cleaned = re.sub(r':::youtube\[.*?\]\{.*?\}', '', cleaned)
        
        # Clean up whitespace
        cleaned = re.sub(r'\n\s*\n', '\n\n', cleaned)
        cleaned = cleaned.strip()
        
        # Truncate if too long (keep first 5000 characters for manageable chunk sizes)
        if len(cleaned) > 5000:
            cleaned = cleaned[:5000] + "..."
        
        return cleaned
    
    def store_publications_in_db(self, publications: List[Dict[str, Any]]):
        """Store publications in database"""
        with app.app_context():
            for pub_data in publications:
                try:
                    # Check if publication already exists
                    existing = Publication.query.filter_by(id=pub_data['id']).first()
                    if existing:
                        logger.debug(f"Publication {pub_data['id']} already exists")
                        continue
                    
                    # Clean the description
                    cleaned_description = self.clean_description(pub_data.get('publication_description', ''))
                    
                    publication = Publication(
                        id=pub_data['id'],
                        username=pub_data.get('username', ''),
                        license=pub_data.get('license', ''),
                        title=pub_data.get('title', ''),
                        description=cleaned_description
                    )
                    
                    db.session.add(publication)
                    logger.debug(f"Added publication: {publication.title}")
                    
                except Exception as e:
                    logger.error(f"Error processing publication {pub_data.get('id', 'unknown')}: {e}")
                    continue
            
            try:
                db.session.commit()
                logger.info(f"Successfully stored publications in database")
            except Exception as e:
                logger.error(f"Error committing publications to database: {e}")
                db.session.rollback()
    
    def get_all_publications(self) -> List[Publication]:
        """Get all publications from database"""
        with app.app_context():
            return Publication.query.all()
    
    def create_document_chunks(self, publications: List[Publication]) -> List[Dict[str, Any]]:
        """Create document chunks for vector store"""
        chunks = []
        
        for pub in publications:
            # Create a comprehensive text representation
            full_text = f"Title: {pub.title}\n\n"
            full_text += f"Author: {pub.username}\n\n"
            if pub.license:
                full_text += f"License: {pub.license}\n\n"
            full_text += f"Description: {pub.description}"
            
            # Split into smaller chunks if the text is very long
            max_chunk_size = 1500
            if len(full_text) <= max_chunk_size:
                chunks.append({
                    'id': pub.id,
                    'text': full_text,
                    'metadata': {
                        'title': pub.title,
                        'username': pub.username,
                        'license': pub.license,
                        'pub_id': pub.id
                    }
                })
            else:
                # Split into smaller chunks
                words = full_text.split()
                current_chunk = []
                current_length = 0
                
                for word in words:
                    if current_length + len(word) + 1 > max_chunk_size and current_chunk:
                        chunk_text = ' '.join(current_chunk)
                        chunks.append({
                            'id': f"{pub.id}_{len(chunks)}",
                            'text': chunk_text,
                            'metadata': {
                                'title': pub.title,
                                'username': pub.username,
                                'license': pub.license,
                                'pub_id': pub.id
                            }
                        })
                        current_chunk = []
                        current_length = 0
                    
                    current_chunk.append(word)
                    current_length += len(word) + 1
                
                # Add the last chunk
                if current_chunk:
                    chunk_text = ' '.join(current_chunk)
                    chunks.append({
                        'id': f"{pub.id}_{len(chunks)}",
                        'text': chunk_text,
                        'metadata': {
                            'title': pub.title,
                            'username': pub.username,
                            'license': pub.license,
                            'pub_id': pub.id
                        }
                    })
        
        logger.info(f"Created {len(chunks)} document chunks")
        return chunks

def initialize_data():
    """Initialize data processing - load and store publications"""
    processor = PublicationProcessor()
    
    # Load publications from the attached JSON file
    publications = processor.load_publications_from_json('attached_assets/project_1_publications_1749806909080.json')
    
    if publications:
        # Store in database
        processor.store_publications_in_db(publications)
        logger.info("Data initialization completed")
    else:
        logger.error("No publications loaded - data initialization failed")
