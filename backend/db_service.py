from backend.models import Question, db


class dbService:
    # Fetch all questions
    @staticmethod
    def get_all_questions():
        questions = Question.query.all()
        output = [
            {
                'id': question.id,
                'text': question.text,
                'options': question.options.split(','),  # Convert string to list
            }
            for question in questions
        ]
        return output

    # Get a single question by ID
    @staticmethod
    def get_question_by_id(question_id):
        return Question.query.get(question_id)

    # Evaluate the user's answer
    @staticmethod
    def check_answer(question_id, user_answer):
        # Retrieve the question by its ID
        question = Question.query.get(question_id)
        if not question:
            return {'error': 'Question not found'}  # Return an error if question doesn't exist
        # Check whether the answer is correct
        is_correct = question.correct_answer.lower() == user_answer.lower()
        return {'correct': is_correct}

    @staticmethod
    def handle_quiz_step(question_id, user_answer, current_index, current_score):
        print("Xd")
        questions_raw = Question.query.all()
        questions = [
            {
                'id': q.id,
                'text': q.text,
                'options': q.options.split(','),
                'correct_answer': q.correct_answer
            }
            for q in questions_raw
        ]
        print(len(questions))
        if current_index >= len(questions):
            return {
                'finished': True,
                'score': current_score,
                'total': len(questions)
            }

        current_question = questions[current_index]
        is_correct = current_question['correct_answer'].lower() == user_answer.lower()
        updated_score = current_score + 1 if is_correct else current_score

        next_index = current_index + 1
        if next_index < len(questions):
            next_question = {
                'id': questions[next_index]['id'],
                'text': questions[next_index]['text'],
                'options': questions[next_index]['options']
            }
            return {
                'question': next_question,
                'question_index': next_index,
                'score': updated_score
            }
        else:
            return {
                'finished': True,
                'score': updated_score,
                'total': len(questions)
            }

    @staticmethod
    def populate_dummy_data():
        # Define dummy questions
        dummy_questions = [
            {
                'text': 'What is the capital of France?',
                'correct_answer': 'Paris',
                'options': 'Paris,London,Berlin,Madrid'
            },
            {
                'text': 'What is 2 + 2?',
                'correct_answer': '4',
                'options': '3,4,5,6'
            },
            {
                'text': 'Who wrote "Romeo and Juliet"?',
                'correct_answer': 'Shakespeare',
                'options': 'Shakespeare,Dickens,Hemingway,Tolkien'
            },
            {
                'text': 'What is the largest planet in the Solar System?',
                'correct_answer': 'Jupiter',
                'options': 'Mars,Venus,Jupiter,Saturn'
            }
        ]
        db.session.query(Question).delete()
        # Add questions to the database
        for question_data in dummy_questions:
            question = Question(
                text=question_data['text'],
                correct_answer=question_data['correct_answer'],
                options=question_data['options']
            )
            db.session.add(question)
        db.session.commit()
