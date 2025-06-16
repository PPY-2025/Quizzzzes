let currentQuestion = null;
let score = 0;
let questionIndex = 0;
let selectedOption = null;
let quizId = null;

function getQuizId() {
    const params = new URLSearchParams(window.location.search);
    return params.get('quiz_id');
}

async function startQuiz() {
    quizId = getQuizId();
    const res = await fetch(`http://127.0.0.1:5000/start?quiz_id=${quizId}`);
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
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            question_id: currentQuestion.id,
            user_answer: selectedOption,
            question_index: questionIndex,
            score: score,
            quiz_id: quizId
        })
    });

    const data = await res.json();

    if (data.finished) {
        const container = document.getElementById('question-container');
        container.innerHTML = `<h3>Quiz finished! Your score: ${data.score}/${data.total}</h3>`;

        // Ukryj oryginalny przycisk submit
        const submitBtn = document.getElementById('submit-answer');
        submitBtn.style.display = 'none';

        // Stwórz nowy przycisk try again
        const retryBtn = document.createElement('button');
        retryBtn.textContent = 'Try Again';
        retryBtn.onclick = () => location.reload();

        const goHomeBtn = document.createElement('button');
        goHomeBtn.textContent = '🏠';
        goHomeBtn.onclick = () => {
            window.location.href = '/';
        };

        container.appendChild(retryBtn);
        container.appendChild(goHomeBtn);
    } else {
        score = data.score;
        questionIndex = data.question_index;
        showQuestion(data.question);
        document.getElementById('submit-answer').disabled = true;
    }
};

// Start quiz
startQuiz();
