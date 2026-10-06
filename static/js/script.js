(() => {
  "use strict";
  const $ = (id) => document.getElementById(id);

  /* ---------- Navbar ---------- */
  const navToggle = $("navToggle"), navLinks = $("navLinks");
  navToggle.addEventListener("click", () => {
    const open = navLinks.classList.toggle("open");
    navToggle.setAttribute("aria-expanded", open);
  });
  navLinks.querySelectorAll("a").forEach(a => a.addEventListener("click", () => navLinks.classList.remove("open")));

  /* ---------- Hero particle network ---------- */
  const canvas = $("heroCanvas"), ctx = canvas.getContext("2d");
  let W, H, points = [];
  function resize() {
    W = canvas.width = canvas.offsetWidth;
    H = canvas.height = canvas.offsetHeight;
    const n = Math.min(70, Math.floor((W * H) / 18000));
    points = Array.from({ length: n }, () => ({
      x: Math.random() * W, y: Math.random() * H,
      vx: (Math.random() - 0.5) * 0.4, vy: (Math.random() - 0.5) * 0.4,
    }));
  }
  resize(); window.addEventListener("resize", resize);
  (function tick() {
    ctx.clearRect(0, 0, W, H);
    for (const p of points) {
      p.x += p.vx; p.y += p.vy;
      if (p.x < 0 || p.x > W) p.vx *= -1;
      if (p.y < 0 || p.y > H) p.vy *= -1;
      ctx.fillStyle = "rgba(148,163,184,0.5)";
      ctx.beginPath(); ctx.arc(p.x, p.y, 1.6, 0, 7); ctx.fill();
    }
    for (let i = 0; i < points.length; i++) for (let j = i + 1; j < points.length; j++) {
      const a = points[i], b = points[j], d = Math.hypot(a.x - b.x, a.y - b.y);
      if (d < 120) {
        ctx.strokeStyle = `rgba(99,102,241,${0.18 * (1 - d / 120)})`;
        ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
      }
    }
    requestAnimationFrame(tick);
  })();

  /* ---------- Counters ---------- */
  const textInput = $("textInput");
  function updateCounts() {
    const t = textInput.value;
    $("charCount").textContent = `${t.length} characters`;
    const words = t.trim() ? t.trim().split(/\s+/).length : 0;
    $("wordCount").textContent = `${words} words`;
  }
  textInput.addEventListener("input", updateCounts);

  $("clearBtn").addEventListener("click", () => {
    textInput.value = ""; updateCounts(); $("errorMsg").hidden = true; textInput.focus();
  });

  document.querySelectorAll(".chip").forEach(chip =>
    chip.addEventListener("click", () => {
      textInput.value = chip.dataset.example; updateCounts(); textInput.focus();
      document.getElementById("analyzer").scrollIntoView({ behavior: "smooth" });
    })
  );

  /* ---------- Charts ---------- */
  Chart.defaults.color = "#8b98ad";
  Chart.defaults.borderColor = "rgba(148,163,184,0.12)";
  const vaderChart = new Chart($("vaderChart"), {
    type: "doughnut",
    data: { labels: ["Positive", "Negative", "Neutral"], datasets: [{ data: [0, 0, 1], backgroundColor: ["#34d399", "#f43f5e", "#94a3b8"], borderWidth: 0 }] },
    options: { plugins: { legend: { position: "bottom" } }, cutout: "62%" },
  });
  const statsChart = new Chart($("statsChart"), {
    type: "bar",
    data: { labels: ["Words", "Characters", "Sentences"], datasets: [{ label: "Count", data: [0, 0, 0], backgroundColor: ["#6366f1", "#22d3ee", "#8b5cf6"], borderRadius: 8 }] },
    options: { plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true } } },
  });

  /* ---------- History ---------- */
  const HISTORY_KEY = "sentix_history";
  function loadHistory() { try { return JSON.parse(localStorage.getItem(HISTORY_KEY)) || []; } catch { return []; } }
  function saveHistory(h) { localStorage.setItem(HISTORY_KEY, JSON.stringify(h.slice(0, 8))); }
  function renderHistory() {
    const h = loadHistory(), el = $("historyList");
    if (!h.length) { el.innerHTML = '<p class="muted">No analyses yet.</p>'; return; }
    el.innerHTML = h.map(item => `
      <div class="history-item">
        <span class="history-text" title="${item.text.replace(/"/g, "&quot;")}">${item.text}</span>
        <span class="sent ${item.sentiment}">${item.sentiment.toUpperCase()}</span>
        <span class="history-score">${item.score >= 0 ? "+" : ""}${item.score.toFixed(2)}</span>
        <span class="history-time">${item.time}</span>
      </div>`).join("");
  }
  $("clearHistory").addEventListener("click", () => { localStorage.removeItem(HISTORY_KEY); renderHistory(); });
  renderHistory();

  /* ---------- Analysis ---------- */
  function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

  async function runPipelineAnimation() {
    const steps = document.querySelectorAll("#pipeline [data-step]");
    const bar = $("progressBar");
    $("pipeline").hidden = false;
    steps.forEach(s => { s.classList.remove("active", "done"); });
    for (let i = 0; i < steps.length; i++) {
      steps[i].classList.add("active");
      bar.style.width = `${((i + 1) / steps.length) * 100}%`;
      await sleep(280);
      steps[i].classList.remove("active"); steps[i].classList.add("done");
    }
    await sleep(150);
  }

  function animateGauge(score) {
    const arc = $("gaugeArc");
    const frac = (score + 1) / 2; // -1..1 -> 0..1
    arc.style.strokeDashoffset = String(267 * (1 - frac));
  }

  function showResult(data) {
    $("resultEmpty").hidden = true;
    $("resultBody").hidden = false;
    const badge = $("sentimentBadge");
    badge.textContent = data.sentiment.toUpperCase();
    badge.className = `sentiment-badge ${data.sentiment}`;
    $("scoreValue").textContent = (data.score >= 0 ? "+" : "") + data.score.toFixed(2);
    $("intensityValue").textContent = data.intensity.toFixed(2);
    $("interpretation").textContent = `"${data.interpretation}"`;
    animateGauge(data.score);

    vaderChart.data.datasets[0].data = [data.vader.positive, data.vader.negative, data.vader.neutral];
    vaderChart.update();
    const s = data.text_statistics;
    statsChart.data.datasets[0].data = [s.words, s.characters, s.sentences];
    statsChart.update();
    $("mWords").textContent = s.words;
    $("mChars").textContent = s.characters;
    $("mSentences").textContent = s.sentences;
    $("mAvg").textContent = s.avg_word_length;
    $("mIntensity").textContent = data.intensity.toFixed(2);
  }

  $("analyzeBtn").addEventListener("click", async () => {
    const text = textInput.value.trim();
    const err = $("errorMsg");
    err.hidden = true;
    if (!text) { err.textContent = "Please enter some text to analyze."; err.hidden = false; return; }

    $("analyzeBtn").disabled = true;
    try {
      const [res] = await Promise.all([
        fetch("/analyze", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ text }) }),
        runPipelineAnimation(),
      ]);
      const data = await res.json();
      if (!res.ok) { err.textContent = data.error || "Analysis failed."; err.hidden = false; $("pipeline").hidden = true; return; }
      showResult(data);
      const h = loadHistory();
      h.unshift({ text: text.slice(0, 120), sentiment: data.sentiment, score: data.score, time: new Date().toLocaleTimeString() });
      saveHistory(h); renderHistory();
    } catch {
      err.textContent = "Could not reach the server. Is Flask running?"; err.hidden = false;
    } finally {
      $("analyzeBtn").disabled = false;
    }
  });
})();
