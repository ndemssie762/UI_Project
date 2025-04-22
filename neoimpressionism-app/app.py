from flask import Flask, render_template, session, request, redirect, url_for, jsonify
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Lesson and quiz data (normally in JSON, inlined for demo)
lessons = [
    {
        "id": 1,
        "title": "What is Neo-Impressionism?",
        "content": "Neo-Impressionism reinterprets classic impressionist techniques by using systematic dots of color (pointillism) that blend optically.<br>It focuses on scientific color theory to create vibrant, luminous works.",
        "image": "https://cdn.mathpix.com/cropped/2025_04_22_593adf460ff292e3c0d0g-02.jpg?height=521&width=709&top_left_y=419&top_left_x=1377"
    },
    {
        "id": 2,
        "title": "Understanding Pointillism",
        "content": "Pointillism involves applying hundreds of tiny dots of pure color in patterns so they blend from a distance.<br>This technique creates a luminous effect and adds depth to the artwork.",
        "image": "https://cdn.mathpix.com/cropped/2025_04_22_593adf460ff292e3c0d0g-03.jpg?height=496&width=893&top_left_y=621&top_left_x=801"
    },
    {
        "id": 3,
        "title": "Exploring Color Theory in Neo-Impressionism",
        "content": "Artists use complementary colors side by side to create contrast and harmony.<br>The optical blending of these colors intensifies the artwork's vibrancy.",
        "image": "https://cdn.mathpix.com/cropped/2025_04_22_593adf460ff292e3c0d0g-04.jpg?height=440&width=1094&top_left_y=629&top_left_x=699"
    },
    {
        "id": 4,
        "title": "Brushwork & Texture",
        "content": "Neo-Impressionism requires precise, controlled brush strokes to define form and create texture.<br>This deliberate application enhances the optical mixing and overall effect of the painting.",
        "image": "https://cdn.mathpix.com/cropped/2025_04_22_593adf460ff292e3c0d0g-05.jpg?height=713&width=617&top_left_y=361&top_left_x=1337"
    },
    {
        "id": 5,
        "title": "Identifying Visual Patterns",
        "content": "Look for consistent visual cues: repeated dotted patterns, systematic color blocks, and well-defined light/shadow transitions.<br>Compare these patterns to those in traditional Impressionism to notice the distinct Neo-Impressionist style.",
        "image": "https://cdn.mathpix.com/cropped/2025_04_22_593adf460ff292e3c0d0g-06.jpg?height=441&width=859&top_left_y=676&top_left_x=1203"
    },
    {
        "id": 6,
        "title": "Summary of Key Techniques",
        "content": "<ul><li>Pointillism: Using tiny dots of color to create optical blending.</li><li>Color Theory: Strategic placement of complementary colors for vibrant effects.</li><li>Brushwork: Precision strokes that enhance texture and form.</li><li>Visual Patterns: Recognizing consistent design elements unique to the style.</li></ul>Now, let's test your understanding with a quick quiz!",
        "image": ""
    }
]

quiz_questions = [
    {
        "id": 1,
        "question": "Neo-Impressionist artists often placed complementary colors next to each other. What effect does this create?",
        "options": [
            "Makes the painting look dull and muted",
            "Makes colors appear brighter and more vibrant",
            "Creates a blurry effect",
            "Makes the painting appear black and white"
        ],
        "correct": 1
    },
    {
        "id": 2,
        "question": "Look at Paul Signac's painting The Pine Tree at Saint-Tropez. Which technique indicates that this is a Neo-Impressionist painting?",
        "options": [
            "Tiny dots of pure color placed carefully so they blend optically from a distance.",
            "Visible brush strokes with large patches of color mixing directly on the canvas.",
            "Smooth gradients with blurred outlines.",
            "Thick, three-dimensional textures using a palette knife."
        ],
        "image": "https://cdn.mathpix.com/cropped/2025_04_22_593adf460ff292e3c0d0g-09.jpg?height=571&width=715&top_left_y=448&top_left_x=1345",
        "correct": 0
    },
    {
        "id": 3,
        "question": "Georges Seurat's paintings often pair complementary colors side-by-side. What visual effect does this produce?",
        "options": [
            "It creates a vibrant and luminous visual effect.",
            "It produces sharp, geometric shapes.",
            "It causes colors to appear faded or washed out.",
            "It darkens the painting overall."
        ],
        "image": "https://cdn.mathpix.com/cropped/2025_04_22_593adf460ff292e3c0d0g-10.jpg?height=610&width=496&top_left_y=425&top_left_x=1458",
        "correct": 0
    },
    {
        "id": 4,
        "question": "What best describes the intent behind the controlled, dot-based brushwork in Neo-Impressionism?",
        "options": [
            "To capture rapid movement with spontaneous strokes.",
            "To imitate photographic realism with detailed brush strokes.",
            "To obscure figures and create abstract, unclear forms.",
            "To carefully manage how colors blend optically, creating harmony and brightness."
        ],
        "image": "https://cdn.mathpix.com/cropped/2025_04_22_593adf460ff292e3c0d0g-11.jpg?height=546&width=655&top_left_y=448&top_left_x=1382",
        "correct": 3
    },
    {
        "id": 5,
        "question": "Compared to Impressionism, Neo-Impressionism is best distinguished by:",
        "options": [
            "Using brighter subject matter and happier scenes.",
            "Frequent use of black outlines and contours.",
            "Precise dots of color placed methodically rather than loose brushstrokes.",
            "A greater emphasis on abstract geometric forms."
        ],
        "image": "https://cdn.mathpix.com/cropped/2025_04_22_593adf460ff292e3c0d0g-12.jpg?height=499&width=859&top_left_y=484&top_left_x=1216",
        "correct": 2
    }
]

@app.route('/')
def home():
    session.clear()
    return render_template('base.html', page='home')

@app.route('/learn/<int:lesson_id>')
def learn(lesson_id):
    if 'progress' not in session:
        session['progress'] = {'lessons_visited': [], 'quiz_answers': {}, 'timestamps': {}}
    session['progress']['lessons_visited'].append(lesson_id)
    session['progress']['timestamps'][f'lesson_{lesson_id}'] = datetime.now().isoformat()
    lesson = lessons[lesson_id-1]
    return render_template('base.html', page='learn', lesson=lesson, lesson_id=lesson_id, total_lessons=len(lessons))

@app.route('/quiz/<int:question_id>', methods=['GET', 'POST'])
def quiz(question_id):
    if 'progress' not in session:
        session['progress'] = {'lessons_visited': [], 'quiz_answers': {}, 'timestamps': {}}
    if request.method == 'POST':
        data = request.get_json()
        session['progress']['quiz_answers'][str(question_id)] = data['answer']
        return jsonify(success=True)
    question = quiz_questions[question_id-1]
    return render_template('base.html', page='quiz', question=question, question_id=question_id, total_questions=len(quiz_questions))

@app.route('/results')
def results():
    answers = session.get('progress', {}).get('quiz_answers', {})
    score = 0
    for i, q in enumerate(quiz_questions, start=1):
        user_ans = int(answers.get(str(i), -1))
        if user_ans == q['correct']:
            score += 1
    return render_template('results.html', score=score, total=len(quiz_questions), quiz_questions=quiz_questions, answers=answers)

if __name__ == '__main__':
    app.run(debug=True)
