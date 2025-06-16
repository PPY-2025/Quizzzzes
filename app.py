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
        quiz_id = request.args.get('quiz_id', type=int)
        if not quiz_id:
            return jsonify({"error": "Missing quiz_id parameter"}), 400

        questions = dbService.get_questions_by_quiz_id(quiz_id)
        if questions:
            return jsonify({
                "question": questions[0],
                "question_index": 0,
                "score": 0,
                "quiz_id": quiz_id
            })
        else:
            return jsonify({"error": "No questions found for quiz"}), 404

    @app.route('/submit_answer', methods=['POST'])
    def submit_answer():
        data = request.get_json()
        quiz_id = data.get('quiz_id')
        if not quiz_id:
            return jsonify({"error": "Missing quiz_id in request"}), 400

        result = dbService.handle_quiz_step(
            question_id=data['question_id'],
            user_answer=data['user_answer'],
            current_index=data['question_index'],
            current_score=data['score'],
            quiz_id=quiz_id
        )
        return jsonify(result)

    @app.route('/quizzes', methods=['GET'])
    def get_quizzes():
        quizzes = dbService.get_quizzes(limit=10)
        return jsonify(quizzes)

    @app.route('/quiz.html')
    def serve_quiz():
        return app.send_static_file('quiz.html')

    return app
