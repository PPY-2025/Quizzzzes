from backend.models import Question, db, Quiz


class dbService:
    @staticmethod
    def get_quizzes(limit=10):
        quizzes = Quiz.query.limit(limit).all()
        return [{"id": q.id, "name": q.name} for q in quizzes]

    @staticmethod
    def get_questions_by_quiz_id(quiz_id):
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return []
        return [
            {
                "id": question.id,
                "text": question.text,
                "options": question.options.split(",")
            }
            for question in quiz.questions
        ]

    @staticmethod
    def check_answer(question_id, user_answer):
        question = Question.query.get(question_id)
        if not question:
            return {"error": "Question not found"}
        is_correct = question.correct_answer.lower() == user_answer.lower()
        return {"correct": is_correct}

    @staticmethod
    def handle_quiz_step(question_id, user_answer, current_index, current_score, quiz_id):
        questions_raw = Question.query.filter_by(quiz_id=quiz_id).all()
        questions = [
            {
                "id": q.id,
                "text": q.text,
                "options": q.options.split(","),
                "correct_answer": q.correct_answer
            }
            for q in questions_raw
        ]

        if current_index >= len(questions):
            return {
                "finished": True,
                "score": current_score,
                "total": len(questions)
            }

        current_question = questions[current_index]
        is_correct = current_question["correct_answer"].lower() == user_answer.lower()
        updated_score = current_score + 1 if is_correct else current_score

        next_index = current_index + 1
        if next_index < len(questions):
            next_question = {
                "id": questions[next_index]["id"],
                "text": questions[next_index]["text"],
                "options": questions[next_index]["options"]
            }
            return {
                "question": next_question,
                "question_index": next_index,
                "score": updated_score
            }
        else:
            return {
                "finished": True,
                "score": updated_score,
                "total": len(questions)
            }

    @staticmethod
    def populate_dummy_data():
        # Usuń istniejące quizy i pytania
        db.session.query(Question).delete()
        db.session.query(Quiz).delete()

        # Przykładowe quizy z pytaniami
        geography = Quiz(name="Geography Quiz")
        math = Quiz(name="Math Quiz")

        geography.questions = [
            Question(
                text="What is the capital of France?",
                correct_answer="Paris",
                options="Paris,London,Berlin,Madrid"
            ),
            Question(
                text="What is the largest planet in the Solar System?",
                correct_answer="Jupiter",
                options="Mars,Venus,Jupiter,Saturn"
            )
        ]

        math.questions = [
            Question(
                text="What is 2 + 2?",
                correct_answer="4",
                options="3,4,5,6"
            )
        ]

        db.session.add(geography)
        db.session.add(math)
        db.session.commit()
