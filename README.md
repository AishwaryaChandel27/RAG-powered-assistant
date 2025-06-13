# AI/ML Publications RAG Assistant

A Flask-based Retrieval-Augmented Generation (RAG) assistant that answers questions about AI/ML publications using LangChain, FAISS vector search, and OpenAI's GPT models.

## 🚀 Features

- **Intelligent Q&A**: Ask natural language questions about AI/ML research publications
- **RAG Pipeline**: Combines document retrieval with large language model generation
- **Vector Search**: Uses FAISS for efficient similarity search across publication content
- **Web Interface**: Clean, responsive web UI built with Bootstrap
- **Query History**: Track and revisit previous questions and answers
- **System Status**: Monitor system health and vector store statistics
- **Real-time Processing**: Fast document retrieval and response generation

## 🏗️ Architecture

### Components

1. **Data Processing** (`data_processor.py`)
   - Loads and processes publication data from JSON
   - Cleans and chunks documents for optimal retrieval
   - Stores publications in SQLite database

2. **Vector Store** (`vector_store.py`)
   - FAISS-based vector storage for document embeddings
   - OpenAI text-embedding-3-small for generating embeddings
   - Efficient similarity search and ranking

3. **RAG Pipeline** (`rag_pipeline.py`)
   - Coordinates document retrieval and response generation
   - Uses OpenAI GPT-4o for generating contextual answers
   - Implements retrieval-augmented generation workflow

4. **Web Interface** (`routes.py`, `templates/`)
   - Flask-based web application
   - Responsive Bootstrap UI with dark theme
   - Real-time query processing and result display

### Technology Stack

- **Backend**: Flask, SQLAlchemy, LangChain
- **Vector Store**: FAISS for similarity search
- **LLM**: OpenAI GPT-4o and text-embedding-3-small
- **Frontend**: Bootstrap 5, Feather Icons, Vanilla JavaScript
- **Database**: SQLite for query history and publications

## 📋 Prerequisites

- Python 3.8+
- OpenAI API key
- Publications JSON data file

## 🛠️ Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install flask flask-sqlalchemy openai langchain langchain-openai faiss-cpu python-dotenv
   