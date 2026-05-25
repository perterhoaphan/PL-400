/* ===== Stats Charts & Counters ===== */
(function() {
    // Animated counters
    document.querySelectorAll('.counter').forEach(el => {
        const target = parseFloat(el.dataset.target);
        const isFloat = target % 1 !== 0;
        const duration = 1200;
        const start = performance.now();

        function animate(now) {
            const elapsed = now - start;
            const progress = Math.min(elapsed / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3);
            const val = eased * target;
            el.textContent = isFloat ? val.toFixed(1) : Math.round(val);
            if (progress < 1) requestAnimationFrame(animate);
        }
        requestAnimationFrame(animate);
    });

    // Chart.js defaults
    Chart.defaults.color = 'rgba(255,255,255,0.7)';
    Chart.defaults.borderColor = 'rgba(255,255,255,0.08)';
    Chart.defaults.font.family = 'Inter, sans-serif';

    // Score line chart
    const scoreCtx = document.getElementById('scoreChart');
    if (scoreCtx) {
        new Chart(scoreCtx, {
            type: 'line',
            data: {
                labels: STATS_DATA.dates.map((d, i) => `Lần ${i + 1}`),
                datasets: [{
                    label: 'Điểm (%)',
                    data: STATS_DATA.scores,
                    borderColor: '#a78bfa',
                    backgroundColor: 'rgba(167, 139, 250, 0.1)',
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#a78bfa',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 5,
                    pointHoverRadius: 8
                }, {
                    label: 'Điểm đạt (80%)',
                    data: Array(STATS_DATA.scores.length).fill(80),
                    borderColor: 'rgba(251, 146, 60, 0.6)',
                    borderDash: [8, 4],
                    pointRadius: 0,
                    fill: false
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: true, position: 'top' }
                },
                scales: {
                    y: { min: 0, max: 100, ticks: { callback: v => v + '%' } }
                }
            }
        });
    }

    // Pass/Fail doughnut chart
    const passCtx = document.getElementById('passChart');
    if (passCtx) {
        new Chart(passCtx, {
            type: 'doughnut',
            data: {
                labels: ['Đạt', 'Không đạt'],
                datasets: [{
                    data: [STATS_DATA.pass_count, STATS_DATA.fail_count],
                    backgroundColor: ['rgba(52, 211, 153, 0.8)', 'rgba(248, 113, 113, 0.8)'],
                    borderColor: ['rgba(52, 211, 153, 1)', 'rgba(248, 113, 113, 1)'],
                    borderWidth: 2,
                    hoverOffset: 10
                }]
            },
            options: {
                responsive: true,
                cutout: '65%',
                plugins: {
                    legend: { position: 'bottom' }
                }
            }
        });
    }
})();
