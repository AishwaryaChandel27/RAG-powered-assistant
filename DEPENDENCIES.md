# Project Dependencies

This project uses `pyproject.toml` for dependency management. Below are the dependencies in requirements.txt format for reference:

```
email-validator>=2.2.0
faiss-cpu>=1.11.0
flask>=3.1.1
flask-sqlalchemy>=3.1.1
gunicorn>=23.0.0
langchain>=0.3.25
langchain-community>=0.3.25
langchain-openai>=0.3.22
numpy>=2.3.0
openai>=1.86.0
psycopg2-binary>=2.9.10
sqlalchemy>=2.0.41
werkzeug>=3.1.3
```

## Dependency Categories

### Web Framework
- **flask**: Core web framework
- **flask-sqlalchemy**: Database ORM integration
- **gunicorn**: Production WSGI server
- **werkzeug**: WSGI utilities and tools

### AI/ML Stack
- **openai**: OpenAI API client for GPT and embeddings
- **langchain**: Framework for LLM applications
- **langchain-community**: Community integrations
- **langchain-openai**: OpenAI-specific integrations

### Search & Data Processing
- **faiss-cpu**: Fast similarity search and clustering
- **numpy**: Numerical computing library
- **email-validator**: Email validation utilities

### Database Support
- **sqlalchemy**: Database toolkit and ORM
- **psycopg2-binary**: PostgreSQL database adapter

## Installation

The project uses modern Python packaging with `pyproject.toml`. Dependencies are automatically managed through the Replit environment.

For manual installation elsewhere:
```bash
pip install -e .
```

## Environment Variables Required

- `OPENAI_API_KEY`: Required for AI functionality
- `SESSION_SECRET`: Optional, for Flask sessions
- `DATABASE_URL`: Optional, defaults to SQLite