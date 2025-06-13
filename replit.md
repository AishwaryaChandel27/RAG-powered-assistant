# AI/ML Publications RAG Assistant

## Overview

This is a Flask-based Retrieval-Augmented Generation (RAG) system designed to enable intelligent querying of AI/ML research publications. The application processes a curated collection of research publications and provides contextual answers through an interactive web interface, combining document retrieval with AI-powered response generation.

## System Architecture

### Backend Architecture
- **Framework**: Flask web application with SQLAlchemy ORM
- **Database**: SQLite for development (configurable to PostgreSQL via DATABASE_URL)
- **AI Integration**: OpenAI GPT models for response generation and embeddings
- **Search Engine**: Dual approach - simple text-based search (fallback) and FAISS vector search (primary)
- **Session Management**: Flask sessions with configurable secret key

### Frontend Architecture
- **UI Framework**: Bootstrap 5 with responsive design
- **Theme Support**: Light/dark theme toggle with localStorage persistence
- **Icons**: Feather icons for consistent visual elements
- **Interactivity**: Vanilla JavaScript for theme management and example queries

### Data Processing Pipeline
- **Publication Ingestion**: JSON-based data loading from attached assets
- **Content Cleaning**: Markdown removal, image filtering, and text normalization
- **Chunking Strategy**: Large documents split into manageable, searchable segments
- **Vector Embeddings**: OpenAI text-embedding-3-small model for semantic search

## Key Components

### Core Modules

1. **app.py**: Application factory and configuration
   - Database initialization with SQLAlchemy
   - Environment-based configuration management
   - Proxy middleware for deployment compatibility

2. **models.py**: Database schema definitions
   - `Publication`: Stores processed research papers with metadata
   - `QueryHistory`: Tracks user queries and system responses

3. **data_processor.py**: Publication data handling
   - JSON publication loading with error handling
   - Content cleaning and markdown removal
   - Database storage and retrieval operations

4. **rag_pipeline.py**: Core RAG functionality
   - Document retrieval coordination
   - OpenAI API integration for response generation
   - Query processing and context assembly

5. **simple_search.py**: Text-based search fallback
   - Keyword matching and relevance scoring
   - Fast in-memory search across publications
   - Metadata integration for comprehensive results

6. **vector_store.py**: FAISS-based semantic search
   - OpenAI embeddings generation
   - FAISS index creation and persistence
   - Similarity search with configurable top-k results

### Web Interface Components

1. **routes.py**: Flask route handlers
   - Main query interface (`/`)
   - Question processing (`/ask`)
   - Query history display (`/history`) 
   - System status monitoring (`/status`)

2. **Templates**: Jinja2 templates with Bootstrap styling
   - `base.html`: Common layout with navigation and theme support
   - `index.html`: Main query interface with example questions
   - `history.html`: Query history display
   - `status.html`: System monitoring dashboard

## Data Flow

1. **Initialization**: Publications loaded from JSON, processed, and stored in database
2. **Query Processing**: User questions processed through RAG pipeline
3. **Document Retrieval**: Relevant publications retrieved using vector similarity or text search
4. **Response Generation**: OpenAI generates contextual answers from retrieved documents
5. **History Storage**: Queries and responses stored for user reference
6. **Result Display**: Formatted answers presented with source attribution

## External Dependencies

### AI Services
- **OpenAI API**: GPT models for text generation and embeddings
- **Model**: text-embedding-3-small (1536 dimensions) for semantic search
- **Rate Limiting**: Built-in delays to respect API limits

### Python Packages
- **Web Framework**: Flask 3.1.1, Flask-SQLAlchemy 3.1.1
- **AI/ML**: OpenAI 1.86.0, LangChain 0.3.25, FAISS-CPU 1.11.0
- **Database**: SQLAlchemy 2.0.41, psycopg2-binary (PostgreSQL support)
- **Production**: Gunicorn 23.0.0 for WSGI serving

### Frontend Dependencies
- **Bootstrap 5.3.0**: UI framework (CDN)
- **Feather Icons**: Icon library (CDN)
- **Custom CSS/JS**: Theme management and interaction handling

## Deployment Strategy

### Development
- **Local Server**: Flask development server with hot reload
- **Database**: SQLite for simplicity and portability
- **Configuration**: Environment variables with .env support

### Production (Replit)
- **WSGI Server**: Gunicorn with multiple workers
- **Database**: Configurable via DATABASE_URL (SQLite default, PostgreSQL supported)
- **Process Management**: Replit's built-in process management
- **Port Configuration**: External port 80 mapping to internal 5000

### Environment Configuration
- **Required**: OPENAI_API_KEY for AI functionality
- **Optional**: SESSION_SECRET, DATABASE_URL, RAG_TOP_K, MAX_CHUNK_SIZE
- **Deployment**: Autoscale deployment target with proxy fix middleware

## Changelog

Changelog:
- June 13, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.