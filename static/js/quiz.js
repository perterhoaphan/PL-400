/* ===== Quiz Navigation & Logic ===== */
(function() {
    // Start button
    document.getElementById('btnStartQuiz').addEventListener('click', function() {
        document.getElementById('quizStartScreen').style.display = 'none';
        document.getElementById('quizContainer').style.display = 'block';
    });


    let current = 0;
    const total = TOTAL_QUESTIONS;
    const slides = document.querySelectorAll('.question-slide');
    const dots = document.querySelectorAll('.q-dot');
    const progressFill = document.getElementById('progressFill');
    const counter = document.getElementById('questionCounter');
    const categoryEl = document.getElementById('questionCategory');
    const btnPrev = document.getElementById('btnPrev');
    const btnNext = document.getElementById('btnNext');
    const btnSubmit = document.getElementById('btnSubmit');

    function showQuestion(idx) {
        slides.forEach(s => s.style.display = 'none');
        slides[idx].style.display = 'block';
        dots.forEach(d => d.classList.remove('current'));
        dots[idx].classList.add('current');
        current = idx;

        counter.textContent = `Câu ${idx + 1} / ${total}`;
        progressFill.style.width = `${((idx + 1) / total) * 100}%`;

        btnPrev.disabled = idx === 0;
        if (idx === total - 1) {
            btnNext.style.display = 'none';
            btnSubmit.style.display = 'inline-flex';
        } else {
            btnNext.style.display = 'inline-flex';
            btnSubmit.style.display = 'none';
        }
    }

    function updateDotStatus() {
        slides.forEach((slide, i) => {
            const qid = slide.dataset.id;
            const inputs = slide.querySelectorAll(`input[name="q_${qid}"]`);
            const answered = Array.from(inputs).some(inp => inp.checked);
            if (answered) {
                dots[i].classList.add('answered');
            } else {
                dots[i].classList.remove('answered');
            }
        });
    }

    // Option click handlers
    document.querySelectorAll('.option-item').forEach(opt => {
        opt.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            const input = this.querySelector('input');
            if (input.type === 'radio') {
                const name = input.name;
                document.querySelectorAll(`input[name="${name}"]`).forEach(r => {
                    r.checked = false;
                    r.closest('.option-item').classList.remove('selected');
                });
                input.checked = true;
                this.classList.add('selected');
            } else {
                input.checked = !input.checked;
                this.classList.toggle('selected', input.checked);
            }
            updateDotStatus();
        });
    });

    btnPrev.addEventListener('click', () => { if (current > 0) showQuestion(current - 1); });
    btnNext.addEventListener('click', () => { if (current < total - 1) showQuestion(current + 1); });

    dots.forEach(dot => {
        dot.addEventListener('click', () => showQuestion(parseInt(dot.dataset.index)));
    });

    // Submit
    const modal = document.getElementById('submitModal');
    const loadingOverlay = document.getElementById('loadingOverlay');

    btnSubmit.addEventListener('click', () => {
        const answeredCount = document.querySelectorAll('.q-dot.answered').length;
        document.getElementById('answeredCount').textContent = answeredCount;
        const unanswered = total - answeredCount;
        const warningEl = document.getElementById('unansweredWarning');
        const unansweredCountEl = document.getElementById('unansweredCount');
        if (unanswered > 0) {
            warningEl.style.display = 'block';
            unansweredCountEl.textContent = unanswered;
        } else {
            warningEl.style.display = 'none';
        }
        modal.style.display = 'flex';
    });

    document.getElementById('btnCancelSubmit').addEventListener('click', () => {
        modal.style.display = 'none';
    });

    document.getElementById('btnConfirmSubmit').addEventListener('click', () => {
        modal.style.display = 'none';
        loadingOverlay.style.display = 'flex';

        const data = {};
        slides.forEach(slide => {
            const qid = slide.dataset.id;
            const qtype = slide.dataset.type;
            const inputs = slide.querySelectorAll(`input[name="q_${qid}"]`);
            const selected = [];
            inputs.forEach(inp => {
                if (inp.checked) selected.push(parseInt(inp.value));
            });
            data[`q_${qid}`] = selected;
        });

        fetch('/quiz/submit', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        })
        .then(r => r.json())
        .then(result => {
            window.location.href = `/result/${result.session_id}`;
        })
        .catch(err => {
            loadingOverlay.style.display = 'none';
            alert('Lỗi khi nộp bài. Vui lòng thử lại.');
            console.error(err);
        });
    });

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowRight' && current < total - 1) showQuestion(current + 1);
        if (e.key === 'ArrowLeft' && current > 0) showQuestion(current - 1);
    });

    showQuestion(0);
})();
