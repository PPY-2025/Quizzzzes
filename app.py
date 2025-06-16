from flask import Flask, jsonify, request
from backend.models import db
from backend.db_service import dbService
import os

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    os.makedirs(app.instance_path, exist_ok=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(app.instance_path, "database.db")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from flask_cors import CORS
    CORS(app)

    @app.route('/')
    def serve_index():
        return app.send_static_file('index.html')

    @app.route('/start', methods=['GET'])
    def start_quiz():
        questions = dbService.get_all_questions()
        if questions:
            return jsonify({
                "question": questions[0],
                "question_index": 0,
                "score": 0
            })
        else:
            return jsonify({"error": "No questions found"}), 404

    @app.route('/submit_answer', methods=['POST'])
    def submit_answer():
        data = request.get_json()
        result = dbService.handle_quiz_step(
            question_id=data['question_id'],
            user_answer=data['user_answer'],
            current_index=data['question_index'],
            current_score=data['score']
        )
        return jsonify(result)

    return app
