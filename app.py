import json
import os
import random
from flask import Flask, render_template, request, redirect, url_for, jsonify, session

import database

app = Flask(__name__)
app.secret_key = 'pl400-quiz-secret-key-2024'

# Load questions
QUESTIONS_PATH = os.path.join(os.path.dirname(__file__), 'questions.json')
with open(QUESTIONS_PATH, 'r', encoding='utf-8') as f:
    ALL_QUESTIONS = json.load(f)


@app.before_request
def before_first_request():
    database.init_db()


@app.route('/')
def index():
    stats = database.get_stats()
    return render_template('index.html', stats=stats)


@app.route('/quiz')
def quiz():
    questions = random.sample(ALL_QUESTIONS, min(50, len(ALL_QUESTIONS)))
    session['quiz_questions'] = [q['id'] for q in questions]
    return render_template('quiz.html', questions=questions)


@app.route('/quiz/submit', methods=['POST'])
def submit_quiz():
    data = request.get_json()
    quiz_question_ids = session.get('quiz_questions', [])

    if not quiz_question_ids:
        return jsonify({'error': 'No active quiz session'}), 400

    # Create session only when submitting
    session_id = database.create_session(len(quiz_question_ids))

    questions_map = {q['id']: q for q in ALL_QUESTIONS}
    answers = []

    for qid in quiz_question_ids:
        q = questions_map.get(qid)
        if not q:
            continue

        user_answer_key = f'q_{qid}'
        user_selected = data.get(user_answer_key, [])
        if isinstance(user_selected, (int, str)):
            user_selected = [int(user_selected)]
        else:
            user_selected = [int(x) for x in user_selected]

        correct = q['correct']
        is_correct = sorted(user_selected) == sorted(correct)

        answers.append({
            'question_id': qid,
            'selected_answers': user_selected,
            'correct_answers': correct,
            'is_correct': is_correct
        })

    result = database.save_results(session_id, answers)
    result['session_id'] = session_id
    return jsonify(result)


@app.route('/result/<int:session_id>')
def result(session_id):
    data = database.get_session(session_id)
    if not data:
        return redirect(url_for('index'))

    questions_map = {q['id']: q for q in ALL_QUESTIONS}
    enriched_answers = []
    for ans in data['answers']:
        q = questions_map.get(ans['question_id'])
        if q:
            enriched_answers.append({
                **ans,
                'question': q['question'],
                'options': q['options'],
                'explanation': q['explanation'],
                'type': q.get('type', 'single'),
                'category': q['category'],
                'correct_indices': q['correct']
            })

    return render_template('result.html', session=data['session'], answers=enriched_answers)


@app.route('/history')
def history():
    sessions = database.get_all_sessions()
    return render_template('history.html', sessions=sessions)


@app.route('/history/delete/<int:session_id>', methods=['POST', 'DELETE'])
def delete_history(session_id):
    try:
        database.delete_session(session_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/stats')
def stats():
    data = database.get_stats()
    return render_template('stats.html', stats=data)


@app.route('/api/stats')
def api_stats():
    return jsonify(database.get_stats())


if __name__ == '__main__':
    database.init_db()
    app.run(debug=True, port=5000)
