import logging
import json
from flask import render_template, request, jsonify, flash, redirect, url_for
from app import app, db
from models import QueryHistory
from rag_pipeline import rag_pipeline
from data_processor import initialize_data

logger = logging.getLogger(__name__)

@app.route('/')
def index():
    """Main page with query interface"""
    # Initialize RAG pipeline if needed
    if not rag_pipeline.is_initialized:
        try:
            rag_pipeline.initialize()
        except Exception as e:
            logger.error(f"Error initializing RAG pipeline: {e}")
            flash('System initialization failed. Please check configuration.', 'error')
    
    # Get recent queries for display
    recent_queries = db.session.query(QueryHistory).order_by(QueryHistory.timestamp.desc()).limit(5).all()
    
    # Get system status
    status = rag_pipeline.get_system_status()
    
    return render_template('index.html', 
                         recent_queries=recent_queries,
                         system_status=status)

@app.route('/ask', methods=['POST'])
def ask_question():
    """Handle question asking"""
    query = request.form.get('query', '').strip()
    
    if not query:
        flash('Please enter a question.', 'warning')
        return redirect(url_for('index'))
    
    try:
        # Get answer from RAG pipeline
        result = rag_pipeline.answer_question(query)
        
        # Store query in history
        query_history = QueryHistory(
            query=result['query'],
            response=result['answer'],
            retrieved_docs=json.dumps([doc['metadata'] for doc in result['retrieved_docs']]),
            response_time=result['response_time']
        )
        db.session.add(query_history)
        db.session.commit()
        
        return render_template('index.html',
                             query=result['query'],
                             answer=result['answer'],
                             retrieved_docs=result['retrieved_docs'],
                             response_time=result['response_time'],
                             recent_queries=db.session.query(QueryHistory).order_by(QueryHistory.timestamp.desc()).limit(5).all(),
                             system_status=rag_pipeline.get_system_status())
    
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        flash(f'Error processing your question: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/api/ask', methods=['POST'])
def api_ask_question():
    """API endpoint for asking questions"""
    data = request.get_json()
    
    if not data or 'query' not in data:
        return jsonify({'error': 'Query is required'}), 400
    
    query = data['query'].strip()
    if not query:
        return jsonify({'error': 'Query cannot be empty'}), 400
    
    try:
        result = rag_pipeline.answer_question(query)
        
        # Store in history
        query_history = QueryHistory(
            query=result['query'],
            response=result['answer'],
            retrieved_docs=json.dumps([doc['metadata'] for doc in result['retrieved_docs']]),
            response_time=result['response_time']
        )
        db.session.add(query_history)
        db.session.commit()
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"API error processing query: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/status')
def system_status():
    """System status page"""
    status = rag_pipeline.get_system_status()
    return render_template('status.html', status=status)

@app.route('/history')
def query_history():
    """Query history page"""
    page = request.args.get('page', 1, type=int)
    queries = db.session.query(QueryHistory).order_by(QueryHistory.timestamp.desc()).limit(20).offset((page-1)*20).all()
    return render_template('history.html', queries=queries)

@app.route('/initialize', methods=['POST'])
def initialize_system():
    """Initialize or reinitialize the system"""
    try:
        # Initialize data
        initialize_data()
        
        # Reinitialize RAG pipeline
        rag_pipeline.initialize()
        
        flash('System initialized successfully!', 'success')
    except Exception as e:
        logger.error(f"Error initializing system: {e}")
        flash(f'Error initializing system: {str(e)}', 'error')
    
    return redirect(url_for('index'))

# Initialize data on startup
def initialize_system_startup():
    """Initialize system on startup"""
    try:
        initialize_data()
        rag_pipeline.initialize()
        logger.info("System initialized successfully on startup")
    except Exception as e:
        logger.error(f"Error during startup initialization: {e}")

# Initialize will be done manually via the /initialize endpoint
