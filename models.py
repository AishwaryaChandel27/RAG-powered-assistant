from app import db
from datetime import datetime

class QueryHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    query = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    retrieved_docs = db.Column(db.Text)  # JSON string of retrieved document IDs
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    response_time = db.Column(db.Float)  # Response time in seconds

    def __repr__(self):
        return f'<QueryHistory {self.id}: {self.query[:50]}...>'

class Publication(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    license = db.Column(db.String(50))
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    processed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Publication {self.id}: {self.title[:50]}...>'
