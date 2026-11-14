/* Vision Journey — navigation, progress, quizzes, search. No dependencies. */
(() => {
  "use strict";

  const root = document.body.dataset.root || "";
  const store = {
    get(key, fallback) {
      try {
        const raw = localStorage.getItem(`vj:${key}`);
        return raw ? JSON.parse(raw) : fallback;
      } catch {
        return fallback;
      }
    },
    set(key, value) {
      try {
        localStorage.setItem(`vj:${key}`, JSON.stringify(value));
      } catch {
        /* storage may be unavailable; progress is best-effort */
      }
    },
  };

  /* ------------------------------------------------------------------ theme */
  /* Light is the default; a saved choice (or the inline head script for a dark
     reader) decides otherwise. */
  const theme = store.get("theme", "light");
  document.documentElement.dataset.theme = theme === "dark" ? "dark" : "light";

  document.querySelectorAll("[data-theme-toggle]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const next = document.documentElement.dataset.theme === "light" ? "dark" : "light";
      document.documentElement.dataset.theme = next;
      store.set("theme", next);
    });
  });

  /* -------------------------------------------------------------- mobile nav */
  const menuBtn = document.querySelector("[data-menu-toggle]");
  menuBtn?.addEventListener("click", () => {
    document.querySelector(".nav")?.classList.toggle("is-open");
    document.querySelector("[data-sidebar]")?.classList.toggle("is-open");
    menuBtn.setAttribute("aria-expanded", menuBtn.getAttribute("aria-expanded") === "true" ? "false" : "true");
  });

  /* ---------------------------------------------------------------- progress */
  const done = new Set(store.get("done", []));

  function paintProgress() {
    document.querySelectorAll("[data-lesson-link]").forEach((link) => {
      const key = link.dataset.lessonLink;
      link.classList.toggle("is-done", done.has(key));
      link.setAttribute("data-done", done.has(key) ? "true" : "false");
    });
    document.querySelectorAll("[data-progress-dot]").forEach((dot) => {
      const link = dot.closest("[data-lesson-link]");
      dot.classList.toggle("is-done", link ? done.has(link.dataset.lessonLink) : false);
    });
    const chip = document.querySelector("[data-complete]");
    if (chip) {
      const isDone = done.has(chip.dataset.complete);
      chip.classList.toggle("is-done", isDone);
      const label = chip.querySelector("[data-complete-label]");
      if (label) label.textContent = isDone ? "Completed" : "Mark as complete";
    }
    paintPath();
  }

  /* The guided path: progress bar and a button that points at the next unfinished lesson. */
  function paintPath() {
    const links = [...document.querySelectorAll("[data-lesson-link]")];
    const cta = document.querySelector("[data-continue]");
    const bar = document.querySelector("[data-path-bar]");
    const label = document.querySelector("[data-path-progress]");
    if (!links.length || (!cta && !bar && !label)) return;

    const complete = links.filter((link) => done.has(link.dataset.lessonLink)).length;
    if (label) label.textContent = `${complete} of ${links.length} lessons complete`;
    if (bar) bar.style.width = `${Math.round((complete / links.length) * 100)}%`;
    if (cta) {
      const next = links.find((link) => !done.has(link.dataset.lessonLink));
      if (next) {
        cta.href = next.getAttribute("href");
        cta.textContent = complete ? "Continue where you left off" : "Start lesson 01";
      } else {
        cta.href = links[0].getAttribute("href");
        cta.textContent = "Review from the start";
      }
    }
  }

  document.querySelector("[data-complete]")?.addEventListener("click", (event) => {
    const key = event.currentTarget.dataset.complete;
    if (done.has(key)) done.delete(key);
    else done.add(key);
    store.set("done", [...done]);
    paintProgress();
  });

  /* ----------------------------------------------------------------- quizzes */
  const solved = new Set(store.get("quizzes", []));

  /* A wrong option is eliminated but the rest stay answerable: the lesson holds
     Continue until the check is solved, so locking the question would trap the reader. */
  function settle(quiz, chosen, correct, explanation) {
    const buttons = [...quiz.querySelectorAll(".quiz__option")];
    const feedback = quiz.querySelector(".quiz__feedback");
    if (correct) {
      buttons.forEach((b) => {
        b.disabled = true;
        if (b.dataset.correct === "true") b.classList.add("is-correct");
        else b.classList.add("is-dim");
      });
      quiz.classList.add("is-solved");
    } else if (chosen) {
      chosen.disabled = true;
      chosen.classList.add("is-wrong");
      chosen.classList.remove("is-dim");
    }
    if (feedback && explanation) {
      feedback.hidden = false;
      feedback.innerHTML = correct
        ? `<strong>Correct.</strong> ${explanation}`
        : `<strong>Not quite.</strong> ${explanation} <em>Try another option.</em>`;
    }
  }

  document.querySelectorAll("[data-quiz]").forEach((quiz) => {
    const id = quiz.dataset.quiz;
    const buttons = [...quiz.querySelectorAll(".quiz__option")];

    if (solved.has(id)) {
      const correctBtn = buttons.find((b) => b.dataset.correct === "true");
      settle(quiz, correctBtn, true, "");
      quiz.querySelectorAll(".quiz__option").forEach((b) => b.classList.remove("is-dim"));
      const feedback = quiz.querySelector(".quiz__feedback");
      if (feedback) {
        feedback.hidden = false;
        feedback.innerHTML = "<strong>Solved earlier.</strong> Revisit the section if you want to re-derive it.";
      }
      return;
    }

    buttons.forEach((btn) => {
      btn.addEventListener("click", () => {
        const correct = btn.dataset.correct === "true";
        settle(quiz, btn, correct, btn.dataset.explain || "");
        if (correct) {
          solved.add(id);
          store.set("quizzes", [...solved]);
          document.dispatchEvent(new CustomEvent("vj:quiz-solved", { detail: { id } }));
        }
      });
    });
  });

  /* -------------------------------------------------------------- copy code */
  document.querySelectorAll(".code__copy").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const code = btn.parentElement?.querySelector("code");
      if (!code) return;
      try {
        await navigator.clipboard.writeText(code.textContent || "");
        btn.textContent = "Copied";
        setTimeout(() => (btn.textContent = "Copy"), 1400);
      } catch {
        btn.textContent = "Copy failed";
        setTimeout(() => (btn.textContent = "Copy"), 1400);
      }
    });
  });

  /* ----------------------------------------------------------------- search */
  const overlay = document.querySelector("[data-search]");
  const input = document.querySelector("[data-search-input]");
  const results = document.querySelector("[data-search-results]");
  let index = null;
  let active = 0;
  let matches = [];

  async function loadIndex() {
    if (index) return index;
    try {
      const res = await fetch(`${root}search-index.json`);
      index = await res.json();
    } catch {
      index = [];
    }
    return index;
  }

  function score(entry, terms) {
    const title = entry.title.toLowerCase();
    const course = entry.course.toLowerCase();
    const text = (entry.text || "").toLowerCase();
    let total = 0;
    for (const term of terms) {
      if (title.includes(term)) total += 8;
      if (title.startsWith(term)) total += 6;
      if (course.includes(term)) total += 3;
      if ((entry.snippet || "").toLowerCase().includes(term)) total += 3;
      const hits = text.split(term).length - 1;
      total += Math.min(hits, 6);
    }
    return total;
  }

  function renderResults() {
    if (!results) return;
    if (!matches.length) {
      results.innerHTML = '<p class="search__empty">No lesson matches. Try a broader term.</p>';
      return;
    }
    results.innerHTML = matches
      .map(
        (m, i) =>
          `<a class="search__item${i === active ? " is-active" : ""}" href="${root}${m.url}">` +
          `<strong>${escapeHtml(m.title)}</strong>` +
          `<span>${escapeHtml([m.topic, m.course].filter(Boolean).join(" · "))} · ${escapeHtml(m.snippet || "")}</span></a>`
      )
      .join("");
  }

  function escapeHtml(text) {
    return String(text).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  }

  async function runSearch(term) {
    const terms = term.toLowerCase().trim().split(/\s+/).filter(Boolean);
    if (!terms.length) {
      matches = [];
      renderResults();
      return;
    }
    const data = await loadIndex();
    matches = data
      .map((entry) => ({ entry, s: score(entry, terms) }))
      .filter((x) => x.s > 0)
      .sort((a, b) => b.s - a.s)
      .slice(0, 8)
      .map((x) => x.entry);
    active = 0;
    renderResults();
  }

  function openSearch() {
    if (!overlay) return;
    overlay.hidden = false;
    input?.focus();
    runSearch(input?.value || "");
  }

  function closeSearch() {
    if (overlay) overlay.hidden = true;
  }

  document.querySelectorAll("[data-search-open]").forEach((btn) => btn.addEventListener("click", openSearch));
  overlay?.addEventListener("click", (event) => {
    if (event.target === overlay) closeSearch();
  });
  input?.addEventListener("input", () => runSearch(input.value));

  document.addEventListener("keydown", (event) => {
    const isOpen = overlay && !overlay.hidden;
    if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
      event.preventDefault();
      isOpen ? closeSearch() : openSearch();
      return;
    }
    if (!isOpen) {
      if (event.key === "/" && !/input|textarea|select/i.test(document.activeElement?.tagName || "")) {
        event.preventDefault();
        openSearch();
      }
      return;
    }
    if (event.key === "Escape") closeSearch();
    if (event.key === "ArrowDown" || event.key === "ArrowUp") {
      event.preventDefault();
      if (!matches.length) return;
      active = (active + (event.key === "ArrowDown" ? 1 : -1) + matches.length) % matches.length;
      renderResults();
    }
    if (event.key === "Enter" && matches[active]) window.location.href = `${root}${matches[active].url}`;
  });

  /* ------------------------------------------------------------------- math */
  function renderMath() {
    if (!window.katex) return;
    document.querySelectorAll(".math[data-tex], .math-block[data-tex]").forEach((node) => {
      const display = node.classList.contains("math-block");
      try {
        window.katex.render(node.dataset.tex, node, { throwOnError: false, displayMode: display });
      } catch {
        /* keep the readable plain-text fallback */
      }
    });
  }
  renderMath();
  window.addEventListener("load", renderMath);

  /* ------------------------------------------------------------------- steps */
  /* The engine ships a lesson as steps. Show one at a time, keep the outline
     working for hidden steps, hold Continue while a step's check is unanswered,
     and reveal the footer pager only once the last step is reached. */
  function initSteps() {
    const lesson = document.querySelector(".lesson[data-lesson]");
    const steps = [...document.querySelectorAll(".prose > .step")];
    const bar = document.querySelector("[data-stepctl]");
    if (!lesson || steps.length < 2 || !bar) return;

    const prevBtn = bar.querySelector("[data-step-prev]");
    const nextBtn = bar.querySelector("[data-step-next]");
    const finish = bar.querySelector("[data-step-finish]");
    const gate = bar.querySelector("[data-step-gate]");
    const posEl = bar.querySelector("[data-step-pos]");
    const meter = bar.querySelector("[data-step-meter]");
    const nameEl = bar.querySelector("[data-step-name]");
    const total = steps.length;
    let current = 0;

    /* A step with a check stays closed until that check is answered. */
    function gateOpen(index) {
      return !steps[index].querySelector("[data-quiz]:not(.is-solved)");
    }

    function syncGate() {
      const open = gateOpen(current);
      nextBtn.disabled = !open;
      finish.setAttribute("aria-disabled", open ? "false" : "true");
      if (gate) gate.hidden = open;
      return open;
    }

    function show(index, { scroll = false } = {}) {
      current = Math.max(0, Math.min(total - 1, index));
      steps.forEach((step, i) => {
        step.hidden = i !== current;
        step.classList.toggle("is-current", i === current);
      });
      lesson.classList.add("js-steps");
      lesson.classList.toggle("is-final", current === total - 1);
      bar.hidden = false;
      posEl.textContent = String(current + 1);
      meter.style.width = `${((current + 1) / total) * 100}%`;
      nameEl.textContent = steps[current].dataset.stepTitle || (current === 0 ? "Introduction" : "");
      prevBtn.disabled = current === 0;
      nextBtn.hidden = current === total - 1;
      finish.hidden = current !== total - 1;
      syncGate();
      if (scroll) {
        const anchor = (steps[current].querySelector("h2, h3") || steps[current]).getBoundingClientRect();
        window.scrollTo({ top: Math.max(0, anchor.top + window.scrollY - 88), behavior: "smooth" });
      }
    }

    prevBtn.addEventListener("click", () => show(current - 1, { scroll: true }));
    nextBtn.addEventListener("click", () => {
      if (syncGate()) show(current + 1, { scroll: true });
    });
    finish.addEventListener("click", (event) => {
      if (!syncGate()) event.preventDefault();
    });
    document.addEventListener("vj:quiz-solved", syncGate);

    document.addEventListener("keydown", (event) => {
      if (event.metaKey || event.ctrlKey || event.altKey) return;
      if (/input|textarea|select/i.test(document.activeElement?.tagName || "")) return;
      const search = document.querySelector(".search");
      if (search && !search.hidden) return;
      if (event.key === "ArrowRight") {
        event.preventDefault();
        if (syncGate()) show(current + 1, { scroll: true });
      }
      if (event.key === "ArrowLeft") { event.preventDefault(); show(current - 1, { scroll: true }); }
    });

    /* Outline links point at headings in steps that may be hidden. */
    document.querySelectorAll('.toc a[href^="#"]').forEach((link) => {
      link.addEventListener("click", (event) => {
        const target = document.getElementById(decodeURIComponent(link.hash.slice(1)));
        const step = target?.closest(".step");
        if (!target || !step) return;
        event.preventDefault();
        show(steps.indexOf(step));
        target.scrollIntoView({ block: "start", behavior: "smooth" });
        try { history.replaceState(null, "", link.hash); } catch { /* file:// or blocked history */ }
      });
    });

    const hashed = location.hash ? document.getElementById(decodeURIComponent(location.hash.slice(1))) : null;
    const hashedStep = hashed?.closest(".step");
    show(hashedStep ? steps.indexOf(hashedStep) : 0);
    if (hashed && hashedStep) hashed.scrollIntoView({ block: "start", behavior: "smooth" });
  }

  initSteps();
  paintProgress();
})();
