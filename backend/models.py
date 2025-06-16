from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()


# Define the Question model
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)  # Question text
    correct_answer = db.Column(db.String(255), nullable=False)  # Correct answer
    options = db.Column(db.String(255), nullable=False)  # Comma-separated options
