import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'quiz.db')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS quiz_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_time TEXT NOT NULL,
            end_time TEXT,
            total_questions INTEGER NOT NULL DEFAULT 50,
            correct_answers INTEGER NOT NULL DEFAULT 0,
            score REAL NOT NULL DEFAULT 0,
            passed INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS quiz_answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            selected_answers TEXT NOT NULL,
            correct_answers TEXT NOT NULL,
            is_correct INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (session_id) REFERENCES quiz_sessions(id)
        );
    ''')
    conn.commit()
    conn.close()


def create_session(total_questions=50):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO quiz_sessions (start_time, total_questions) VALUES (?, ?)',
        (datetime.now().isoformat(), total_questions)
    )
    session_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return session_id


def save_results(session_id, answers):
    """
    answers: list of dicts with keys:
        question_id, selected_answers (list), correct_answers (list), is_correct (bool)
    """
    conn = get_db()
    cursor = conn.cursor()

    correct_count = sum(1 for a in answers if a['is_correct'])
    total = len(answers)
    score = round((correct_count / total) * 100, 1) if total > 0 else 0
    passed = 1 if score >= 80 else 0

    cursor.execute(
        '''UPDATE quiz_sessions 
           SET end_time=?, correct_answers=?, score=?, passed=? 
           WHERE id=?''',
        (datetime.now().isoformat(), correct_count, score, passed, session_id)
    )

    for a in answers:
        cursor.execute(
            '''INSERT INTO quiz_answers 
               (session_id, question_id, selected_answers, correct_answers, is_correct)
               VALUES (?, ?, ?, ?, ?)''',
            (
                session_id,
                a['question_id'],
                ','.join(str(x) for x in a['selected_answers']),
                ','.join(str(x) for x in a['correct_answers']),
                1 if a['is_correct'] else 0
            )
        )

    conn.commit()
    conn.close()
    return {'correct': correct_count, 'total': total, 'score': score, 'passed': bool(passed)}


def get_session(session_id):
    conn = get_db()
    session = conn.execute('SELECT * FROM quiz_sessions WHERE id=?', (session_id,)).fetchone()
    answers = conn.execute(
        'SELECT * FROM quiz_answers WHERE session_id=? ORDER BY question_id',
        (session_id,)
    ).fetchall()
    conn.close()
    if session is None:
        return None
    return {
        'session': dict(session),
        'answers': [dict(a) for a in answers]
    }


def get_all_sessions():
    conn = get_db()
    sessions = conn.execute(
        'SELECT * FROM quiz_sessions ORDER BY start_time DESC'
    ).fetchall()
    conn.close()
    return [dict(s) for s in sessions]


def get_stats():
    conn = get_db()
    cursor = conn.cursor()

    total_quizzes = cursor.execute('SELECT COUNT(*) FROM quiz_sessions').fetchone()[0]
    if total_quizzes == 0:
        conn.close()
        return {
            'total_quizzes': 0, 'avg_score': 0, 'max_score': 0,
            'min_score': 0, 'pass_count': 0, 'fail_count': 0,
            'pass_rate': 0, 'scores': [], 'dates': [],
            'category_stats': {}
        }

    avg_score = cursor.execute('SELECT AVG(score) FROM quiz_sessions').fetchone()[0] or 0
    max_score = cursor.execute('SELECT MAX(score) FROM quiz_sessions').fetchone()[0] or 0
    min_score = cursor.execute('SELECT MIN(score) FROM quiz_sessions').fetchone()[0] or 0
    pass_count = cursor.execute('SELECT COUNT(*) FROM quiz_sessions WHERE passed=1').fetchone()[0]
    fail_count = total_quizzes - pass_count

    sessions = cursor.execute(
        'SELECT score, start_time FROM quiz_sessions ORDER BY start_time ASC'
    ).fetchall()
    scores = [s[0] for s in sessions]
    dates = [s[1][:10] for s in sessions]

    conn.close()
    return {
        'total_quizzes': total_quizzes,
        'avg_score': round(avg_score, 1),
        'max_score': round(max_score, 1),
        'min_score': round(min_score, 1),
        'pass_count': pass_count,
        'fail_count': fail_count,
        'pass_rate': round((pass_count / total_quizzes) * 100, 1) if total_quizzes > 0 else 0,
        'scores': scores,
        'dates': dates
    }


def delete_session(session_id):
    conn = get_db()
    conn.execute('DELETE FROM quiz_answers WHERE session_id=?', (session_id,))
    conn.execute('DELETE FROM quiz_sessions WHERE id=?', (session_id,))
    conn.commit()
    conn.close()
