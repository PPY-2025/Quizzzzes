let currentQuestion = null;
let score = 0;
let questionIndex = 0;
let selectedOption = null;

async function startQuiz() {
    const res = await fetch('http://127.0.0.1:5000/start');
    const data = await res.json();
    score = data.score;
    questionIndex = data.question_index;
    showQuestion(data.question);
}

function showQuestion(question) {
    currentQuestion = question;
    selectedOption = null;

    const container = document.getElementById('question-container');
    container.innerHTML = `<h3>${question.text}</h3>`;

    question.options.forEach(option => {
        const btn = document.createElement('button');
        btn.textContent = option;
        btn.onclick = () => {
            selectedOption = option;
            document.getElementById('submit-answer').disabled = false;
        };
        container.appendChild(btn);
    });
}

document.getElementById('submit-answer').onclick = async () => {
    const res = await fetch('http://127.0.0.1:5000/submit_answer', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            question_id: currentQuestion.id,
            user_answer: selectedOption,
            question_index: questionIndex,
            score: score
        })
    });

    const data = await res.json();

    if (data.finished) {
        document.getElementById('question-container').innerHTML = `<h3>Quiz finished! Your score: ${data.score}/${data.total}</h3>`;
        document.getElementById('submit-answer').style.display = 'none';
    } else {
        score = data.score;
        questionIndex = data.question_index;
        showQuestion(data.question);
        document.getElementById('submit-answer').disabled = true;
    }
};

// Start quiz
startQuiz();
