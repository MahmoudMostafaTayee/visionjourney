/* Vision Journey — interactive computer-vision labs. Zero dependencies. */
(() => {
  "use strict";

  const DPR = Math.min(window.devicePixelRatio || 1, 2);

  /* ------------------------------------------------------------------ helpers */

  function el(tag, attrs = {}, html) {
    const node = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (k === "class") node.className = v;
      else if (k === "style") node.style.cssText = v;
      else node.setAttribute(k, v);
    }
    if (html != null) node.innerHTML = html;
    return node;
  }

  function makeCanvas(width, height) {
    const cv = el("canvas", { class: "viz__canvas" });
    cv.width = width * DPR;
    cv.height = height * DPR;
    cv.style.width = "100%";
    cv.style.aspectRatio = `${width} / ${height}`;
    const ctx = cv.getContext("2d");
    ctx.scale(DPR, DPR);
    return { cv, ctx, w: width, h: height };
  }

  function slider({ label, min, max, step, value, format = (v) => v, oninput }) {
    const wrap = el("label", { class: "viz__control" });
    const head = el("span", {}, `${label}<span class="viz__value"></span>`);
    const input = el("input", { type: "range", min, max, step, value });
    const out = head.querySelector(".viz__value");
    out.textContent = format(value);
    input.addEventListener("input", () => {
      const v = Number(input.value);
      out.textContent = format(v);
      oninput(v);
    });
    wrap.append(head, input);
    return wrap;
  }

  function readout(html) {
    return el("div", { class: "viz__readout" }, html);
  }

  function controls(...children) {
    const box = el("div", { class: "viz__controls" });
    box.append(...children.filter(Boolean));
    return box;
  }

  const clamp = (v, a, b) => Math.min(b, Math.max(a, v));

  /* ------------------------------------------------------------ synthetic scene */

  function scene(w, h, seed = 1) {
    // A deterministic little "photograph": sky gradient, sun, hill, a dark object.
    const px = new Float32Array(w * h * 3);
    for (let y = 0; y < h; y++) {
      for (let x = 0; x < w; x++) {
        const u = x / (w - 1);
        const v = y / (h - 1);
        let r = 34 + 40 * v;
        let g = 58 + 30 * (1 - v);
        let b = 96 + 60 * (1 - v);
        // hill
        const hill = 0.72 + 0.10 * Math.sin(u * 4.2 + seed) + 0.05 * Math.sin(u * 11 + 2);
        if (v > hill) {
          r = 28 + 22 * (v - hill);
          g = 62 + 30 * (v - hill);
          b = 44 + 18 * (v - hill);
        }
        // sun
        const dx = u - 0.74;
        const dy = v - 0.26;
        const d = Math.sqrt(dx * dx + dy * dy);
        if (d < 0.13) {
          const k = clamp(1 - d / 0.13, 0, 1);
          r = 210 + 45 * k;
          g = 150 + 40 * k;
          b = 60 + 20 * k;
        }
        // dark box
        if (u > 0.14 && u < 0.33 && v > 0.52 && v < 0.8) {
          r = 18 + 10 * (v - 0.52);
          g = 20 + 10 * (v - 0.52);
          b = 30 + 10 * (v - 0.52);
        }
        const i = (y * w + x) * 3;
        px[i] = r;
        px[i + 1] = g;
        px[i + 2] = b;
      }
    }
    return px;
  }

  function toGray(px, w, h) {
    const g = new Float32Array(w * h);
    for (let i = 0; i < w * h; i++) {
      g[i] = 0.2126 * px[i * 3] + 0.7152 * px[i * 3 + 1] + 0.0722 * px[i * 3 + 2];
    }
    return g;
  }

  function drawGray(ctx, data, w, h, box = {}) {
    const { x = 0, y = 0, cw = ctx.canvas.width / DPR, ch = ctx.canvas.height / DPR } = box;
    const img = ctx.createImageData(w, h);
    for (let i = 0; i < w * h; i++) {
      const v = clamp(Math.round(data[i]), 0, 255);
      img.data[i * 4] = v;
      img.data[i * 4 + 1] = v;
      img.data[i * 4 + 2] = v;
      img.data[i * 4 + 3] = 255;
    }
    const tmp = document.createElement("canvas");
    tmp.width = w;
    tmp.height = h;
    tmp.getContext("2d").putImageData(img, 0, 0);
    ctx.imageSmoothingEnabled = false;
    ctx.drawImage(tmp, x, y, cw, ch);
  }

  function drawRGB(ctx, px, w, h, box = {}) {
    const { x = 0, y = 0, cw = ctx.canvas.width / DPR, ch = ctx.canvas.height / DPR } = box;
    const img = ctx.createImageData(w, h);
    for (let i = 0; i < w * h; i++) {
      img.data[i * 4] = clamp(px[i * 3], 0, 255);
      img.data[i * 4 + 1] = clamp(px[i * 3 + 1], 0, 255);
      img.data[i * 4 + 2] = clamp(px[i * 3 + 2], 0, 255);
      img.data[i * 4 + 3] = 255;
    }
    const tmp = document.createElement("canvas");
    tmp.width = w;
    tmp.height = h;
    tmp.getContext("2d").putImageData(img, 0, 0);
    ctx.imageSmoothingEnabled = false;
    ctx.drawImage(tmp, x, y, cw, ch);
  }

  const css = (name, fallback) =>
    getComputedStyle(document.documentElement).getPropertyValue(name).trim() || fallback;

  /* ----------------------------------------------------------------- 1. convolution */

  const KERNELS = {
    identity: { label: "Identity", w: [0, 0, 0, 0, 1, 0, 0, 0, 0] },
    blur: { label: "Box blur", w: [1, 1, 1, 1, 1, 1, 1, 1, 1], norm: 9 },
    gaussian: { label: "Gaussian", w: [1, 2, 1, 2, 4, 2, 1, 2, 1], norm: 16 },
    sharpen: { label: "Sharpen", w: [0, -1, 0, -1, 5, -1, 0, -1, 0] },
    sobelx: { label: "Sobel X", w: [-1, 0, 1, -2, 0, 2, -1, 0, 1] },
    sobely: { label: "Sobel Y", w: [-1, -2, -1, 0, 0, 0, 1, 2, 1] },
    laplace: { label: "Laplacian", w: [0, 1, 0, 1, -4, 1, 0, 1, 0] },
  };

  function demoConvolution(stage) {
    const W = 26, H = 20;
    const src = toGray(scene(W, H, 2), W, H);
    let key = "sobelx";
    let gain = 1;
    let offset = 0;

    const { cv, ctx, w, h } = makeCanvas(640, 260);
    const picker = el("div", { class: "viz__chips" });
    Object.entries(KERNELS).forEach(([k, def]) => {
      const chip = el("button", { class: "viz__chip", type: "button" }, def.label);
      chip.addEventListener("click", () => {
        key = k;
        [...picker.children].forEach((c) => c.classList.remove("is-active"));
        chip.classList.add("is-active");
        render();
      });
      if (k === key) chip.classList.add("is-active");
      picker.append(chip);
    });

    const out = readout("");

    function conv() {
      const k = KERNELS[key];
      const n = k.norm || 1;
      const res = new Float32Array(W * H);
      for (let y = 1; y < H - 1; y++) {
        for (let x = 1; x < W - 1; x++) {
          let sum = 0;
          for (let ky = -1; ky <= 1; ky++) {
            for (let kx = -1; kx <= 1; kx++) {
              sum += src[(y + ky) * W + (x + kx)] * k.w[(ky + 1) * 3 + (kx + 1)];
            }
          }
          res[y * W + x] = clamp((sum / n) * gain + offset, -255, 510);
        }
      }
      return res;
    }

    function render() {
      const res = conv();
      const pad = 18;
      const cell = Math.min((w - 3 * pad) / (W * 2), (h - 60) / H);
      const top = 34;
      const gw = cell * W;
      const gh = cell * H;

      ctx.clearRect(0, 0, w, h);
      ctx.fillStyle = css("--faint", "#64748b");
      ctx.font = "10px ui-monospace, monospace";
      ctx.fillText("INPUT  26 × 20", pad, 20);
      ctx.fillText(`OUTPUT  ${W - 2} × ${H - 2}   (valid convolution)`, pad * 2 + gw + 26, 20);

      drawGray(ctx, src, W, H, { x: pad, y: top, cw: gw, ch: gh });

      // highlight one 3x3 window
      ctx.strokeStyle = css("--accent", "#22d3ee");
      ctx.lineWidth = 1.4;
      ctx.strokeRect(pad + 11 * cell, top + 7 * cell, cell * 3, cell * 3);

      // kernel matrix
      const kx = pad + gw + 13;
      const ks = 20;
      const k = KERNELS[key];
      ctx.save();
      ctx.translate(kx, top + 34);
      for (let i = 0; i < 9; i++) {
        const v = k.w[i];
        const cx = (i % 3) * (ks + 3);
        const cy = Math.floor(i / 3) * (ks + 3);
        ctx.fillStyle = v === 0 ? "rgba(148,163,184,.12)" : v > 0 ? "rgba(34,211,238,.30)" : "rgba(251,113,133,.30)";
        ctx.fillRect(cx, cy, ks, ks);
        ctx.fillStyle = css("--text", "#e8eef8");
        ctx.font = "9px ui-monospace, monospace";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(String(v), cx + ks / 2, cy + ks / 2 + 1);
      }
      ctx.restore();

      // arrow
      ctx.strokeStyle = css("--line-strong", "#475569");
      ctx.beginPath();
      ctx.moveTo(kx + ks * 3 + 10, top + 50);
      ctx.lineTo(kx + ks * 3 + 30, top + 50);
      ctx.stroke();

      // output
      const ox = pad * 2 + gw + 78;
      const outCell = Math.min((w - ox - pad) / W, (h - top - 10) / H);
      drawGray(ctx, res, W, H, { x: ox, y: top, cw: outCell * W, ch: outCell * H });

      const max = Math.max(...Array.from(res, Math.abs));
      out.innerHTML =
        `kernel <b>${callName(key)}</b> · response range <b>${(-max).toFixed(0)} … ${max.toFixed(0)}</b><br>` +
        `output element = Σ (3×3 patch × kernel) = one pixel of the feature map`;
    }

    function callName(k) {
      return KERNELS[k].label;
    }

    const box = el("div", { class: "viz" });
    box.append(
      picker,
      cv,
      controls(
        slider({ label: "Gain", min: 0.2, max: 3, step: 0.1, value: gain, format: (v) => v.toFixed(1) + "×", oninput: (v) => { gain = v; render(); } }),
        slider({ label: "Brightness", min: -80, max: 80, step: 5, value: 0, format: (v) => (v > 0 ? "+" : "") + v, oninput: (v) => { offset = v; render(); } })
      ),
      out
    );
    stage.append(box);
    render();
  }

  /* ------------------------------------------------------------------- 2. histogram */

  function demoHistogram(stage) {
    const W = 64, H = 48;
    const base = scene(W, H, 4);
    let exposure = 0, contrast = 1, gamma = 1;

    const { cv, ctx, w, h } = makeCanvas(640, 250);
    const out = readout("");

    function adjust() {
      const px = new Float32Array(base.length);
      const c = clamp(contrast, 0.2, 2.5);
      for (let i = 0; i < base.length; i++) {
        let v = base[i] / 255;
        v = Math.pow(clamp(v, 0, 1), 1 / gamma);
        v = (v - 0.5) * c + 0.5;
        v = v * Math.pow(2, exposure);
        px[i] = clamp(v * 255, 0, 255);
      }
      return px;
    }

    function render() {
      const px = adjust();
      ctx.clearRect(0, 0, w, h);
      const imgW = 230, imgH = 172;
      drawRGB(ctx, px, W, H, { x: 14, y: 44, cw: imgW, ch: imgH });

      const hx = imgW + 44, hy = 44, hw = w - hx - 20, hh = 168;
      const bins = new Array(64).fill(0);
      for (let i = 0; i < W * H; i++) {
        const lum = 0.2126 * px[i * 3] + 0.7152 * px[i * 3 + 1] + 0.0722 * px[i * 3 + 2];
        bins[Math.min(63, Math.floor((lum / 256) * 64))]++;
      }
      const peak = Math.max(...bins);
      ctx.strokeStyle = css("--line", "rgba(148,163,184,.2)");
      ctx.strokeRect(hx, hy, hw, hh);
      for (let i = 0; i < 64; i++) {
        const bh = (bins[i] / peak) * (hh - 4);
        const g = Math.round((i / 63) * 255);
        ctx.fillStyle = `rgba(${g},${Math.min(255, g + 30)},255,${0.35 + 0.5 * (bins[i] / peak)})`;
        ctx.fillRect(hx + (i / 64) * hw + 0.5, hy + hh - bh, hw / 64 - 1, bh);
      }

      ctx.fillStyle = css("--faint", "#64748b");
      ctx.font = "10px ui-monospace, monospace";
      ctx.fillText("0", hx, hy + hh + 14);
      ctx.fillText("luminance", hx + hw / 2 - 30, hy + hh + 14);
      ctx.fillText("255", hx + hw - 16, hy + hh + 14);
      ctx.fillStyle = css("--muted", "#94a3b8");
      ctx.font = "10.5px ui-monospace, monospace";
      ctx.fillText("IMAGE 64 × 48", 14, 28);
      ctx.fillText("PANEL HISTOGRAM (64 bins)", hx, 28);

      let clipped = 0;
      for (let i = 0; i < px.length; i += 3) {
        const lum = 0.2126 * px[i] + 0.7152 * px[i + 1] + 0.0722 * px[i + 2];
        if (lum > 253 || lum < 2) clipped++;
      }
      const pct = ((clipped / (W * H)) * 100).toFixed(1);
      out.innerHTML =
        `clipped pixels <b>${pct}%</b> · mean luminance <b>${(bins.reduce((a, b, i) => a + b * (i + 0.5) * 4, 0) / (W * H)).toFixed(0)}</b>` +
        `<br>${Number(pct) > 4 ? "⚠ highlight or shadow detail is being lost at the sensor boundary." : "detail is preserved across the tonal range."}`;
    }

    const box = el("div", { class: "viz" });
    box.append(
      cv,
      controls(
        slider({ label: "Exposure", min: -1.5, max: 1.5, step: 0.1, value: 0, format: (v) => (v > 0 ? "+" : "") + v.toFixed(1) + " EV", oninput: (v) => { exposure = v; render(); } }),
        slider({ label: "Contrast", min: 0.4, max: 2.2, step: 0.05, value: 1, format: (v) => v.toFixed(2), oninput: (v) => { contrast = v; render(); } }),
        slider({ label: "Gamma", min: 0.4, max: 2.4, step: 0.05, value: 1, format: (v) => v.toFixed(2), oninput: (v) => { gamma = v; render(); } })
      ),
      out
    );
    stage.append(box);
    render();
  }

  /* ---------------------------------------------------------------------- 3. edges */

  function demoEdges(stage) {
    const W = 64, H = 48;
    const gray = toGray(scene(W, H, 3), W, H);
    let threshold = 26;
    let mode = "sobel";

    const { cv, ctx, w, h } = makeCanvas(640, 260);
    const out = readout("");
    const picker = el("div", { class: "viz__chips" });
    [["sobel", "Sobel magnitude"], ["laplace", "Laplacian"], ["prewitt", "Prewitt X"]].forEach(([k, label]) => {
      const chip = el("button", { class: "viz__chip" + (k === mode ? " is-active" : ""), type: "button" }, label);
      chip.addEventListener("click", () => {
        mode = k;
        [...picker.children].forEach((c) => c.classList.remove("is-active"));
        chip.classList.add("is-active");
        render();
      });
      picker.append(chip);
    });

    function gradient(x, y) {
      const at = (xx, yy) => gray[clamp(yy, 0, H - 1) * W + clamp(xx, 0, W - 1)];
      const gx = -at(x - 1, y - 1) - 2 * at(x - 1, y) - at(x - 1, y + 1) + at(x + 1, y - 1) + 2 * at(x + 1, y) + at(x + 1, y + 1);
      const gy = -at(x - 1, y - 1) - 2 * at(x, y - 1) - at(x + 1, y - 1) + at(x - 1, y + 1) + 2 * at(x, y + 1) + at(x + 1, y + 1);
      return [gx / 4, gy / 4];
    }

    function render() {
      const mag = new Float32Array(W * H);
      const edge = new Float32Array(W * H);
      let count = 0;
      for (let y = 0; y < H; y++) {
        for (let x = 0; x < W; x++) {
          let gx = 0, gy = 0;
          if (mode === "sobel") [gx, gy] = gradient(x, y);
          else if (mode === "prewitt") {
            const at = (xx, yy) => gray[clamp(yy, 0, H - 1) * W + clamp(xx, 0, W - 1)];
            gx = (-at(x - 1, y - 1) - at(x - 1, y) - at(x - 1, y + 1) + at(x + 1, y - 1) + at(x + 1, y) + at(x + 1, y + 1)) / 3;
          } else {
            const at = (xx, yy) => gray[clamp(yy, 0, H - 1) * W + clamp(xx, 0, W - 1)];
            gx = at(x - 1, y) - at(x + 1, y);
            gy = at(x, y - 1) - at(x, y + 1);
          }
          const m = Math.sqrt(gx * gx + gy * gy);
          mag[y * W + x] = m;
          if (m > threshold) {
            edge[y * W + x] = 255;
            count++;
          }
        }
      }
      const max = Math.max(...Array.from(mag), 1);
      const pad = 16, top = 30;
      const cw = (w - pad * 3) / 2;
      const ch = Math.min((h - top - 14), cw * 0.75);
      ctx.clearRect(0, 0, w, h);
      ctx.fillStyle = css("--faint", "#64748b");
      ctx.font = "10px ui-monospace, monospace";
      ctx.fillText("INPUT", pad, 20);
      ctx.fillText(`THRESHOLDED MAGNITUDE  T=${threshold}`, pad * 2 + cw, 20);
      drawGray(ctx, gray, W, H, { x: pad, y: top, cw, ch });
      drawGray(ctx, edge, W, H, { x: pad * 2 + cw, y: top, cw, ch });
      out.innerHTML = `<b>${count}</b> edge pixels (${((count / (W * H)) * 100).toFixed(1)}%) · max |∇I| = <b>${max.toFixed(1)}</b><br>|∇I| = √(Gx² + Gy²), edge direction = atan2(Gy, Gx)`;
    }

    const box = el("div", { class: "viz" });
    box.append(picker, cv, controls(
      slider({ label: "Threshold", min: 1, max: 160, step: 1, value: threshold, format: (v) => v, oninput: (v) => { threshold = v; render(); } })
    ), out);
    stage.append(box);
    render();
  }

  /* -------------------------------------------------------------------- 4. pinhole */

  function demoPinhole(stage) {
    let focal = 50, distance = 3, height = 1.8;
    const { cv, ctx, w, h } = makeCanvas(640, 280);
    const out = readout("");

    function render() {
      const f = focal / 1000;
      const proj = (height * f) / distance;
      ctx.clearRect(0, 0, w, h);
      const cx = w * 0.55;
      const cy = h / 2;
      const pxPerM = 78;

      // image plane
      ctx.strokeStyle = css("--line-strong", "#475569");
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(cx - 150, 40);
      ctx.lineTo(cx - 150, h - 40);
      ctx.stroke();

      // axis
      ctx.strokeStyle = css("--line", "rgba(148,163,184,.18)");
      ctx.lineWidth = 1;
      ctx.setLineDash([4, 6]);
      ctx.beginPath();
      ctx.moveTo(20, cy);
      ctx.lineTo(w - 20, cy);
      ctx.stroke();
      ctx.setLineDash([]);

      // pinhole
      ctx.fillStyle = css("--accent", "#22d3ee");
      ctx.beginPath();
      ctx.arc(cx, cy, 4, 0, Math.PI * 2);
      ctx.fill();

      // object
      const objX = 60;
      const objH = Math.min(150, height * pxPerM * 0.42);
      ctx.strokeStyle = css("--amber", "#fbbf24");
      ctx.lineWidth = 4;
      ctx.beginPath();
      ctx.moveTo(objX, cy);
      ctx.lineTo(objX, cy - objH);
      ctx.stroke();
      ctx.fillStyle = css("--amber", "#fbbf24");
      ctx.font = "10.5px ui-monospace, monospace";
      ctx.fillText(`h = ${height.toFixed(1)} m`, objX + 8, cy - objH - 8);
      ctx.fillText(`d = ${distance.toFixed(1)} m`, (objX + cx) / 2 - 40, cy + 20);

      // rays
      ctx.strokeStyle = "rgba(251,191,36,.75)";
      ctx.lineWidth = 1.2;
      ctx.beginPath();
      ctx.moveTo(objX, cy - objH);
      ctx.lineTo(cx, cy);
      const imgH = Math.min(120, proj * pxPerM * 0.5);
      ctx.lineTo(cx - 150, cy + imgH);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(objX, cy);
      ctx.lineTo(cx, cy);
      ctx.lineTo(cx - 150, cy);
      ctx.stroke();

      // projected image
      ctx.strokeStyle = css("--violet", "#a78bfa");
      ctx.lineWidth = 4;
      ctx.beginPath();
      ctx.moveTo(cx - 150, cy);
      ctx.lineTo(cx - 150, cy + imgH);
      ctx.stroke();
      ctx.fillStyle = css("--violet", "#a78bfa");
      ctx.fillText(`h' = ${(proj * 1000).toFixed(1)} mm`, cx - 145, cy + imgH + 16);

      // focal marker
      ctx.strokeStyle = css("--muted", "#94a3b8");
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(cx - 150, h - 30);
      ctx.lineTo(cx, h - 30);
      ctx.stroke();
      ctx.fillStyle = css("--muted", "#94a3b8");
      ctx.fillText(`f = ${focal} mm`, cx - 130, h - 36);

      const mag = proj / height;
      out.innerHTML =
        `h′ = f·h/d = <b>${(proj * 1000).toFixed(1)} mm</b> on the sensor · magnification <b>${mag.toFixed(4)}</b><br>` +
        `field of view ≈ <b>${((2 * Math.atan(18 / focal)) * (180 / Math.PI)).toFixed(1)}°</b> horizontally for a 36 mm sensor`;
    }

    const box = el("div", { class: "viz" });
    box.append(cv, controls(
      slider({ label: "Focal length", min: 18, max: 135, step: 1, value: focal, format: (v) => v + " mm", oninput: (v) => { focal = v; render(); } }),
      slider({ label: "Object distance", min: 0.5, max: 10, step: 0.1, value: distance, format: (v) => v.toFixed(1) + " m", oninput: (v) => { distance = v; render(); } }),
      slider({ label: "Object height", min: 0.2, max: 4, step: 0.1, value: height, format: (v) => v.toFixed(1) + " m", oninput: (v) => { height = v; render(); } })
    ), out);
    stage.append(box);
    render();
  }

  /* -------------------------------------------------------------------- 5. stereo */

  function demoStereo(stage) {
    let baseline = 0.12, depth = 2.0, focal = 500;
    const { cv, ctx, w, h } = makeCanvas(640, 270);
    const out = readout("");

    function render() {
      const disp = (focal * baseline) / depth;
      ctx.clearRect(0, 0, w, h);
      const cy = 120;
      const half = 110;
      const cxL = w / 2 - half, cxR = w / 2 + half;

      // cameras
      ctx.fillStyle = css("--panel-2", "#121c2f");
      ctx.strokeStyle = css("--line-strong", "#475569");
      ctx.lineWidth = 1.2;
      [cxL, cxR].forEach((x) => {
        ctx.beginPath();
        ctx.roundRect(x - 18, cy - 16, 36, 30, 5);
        ctx.fill();
        ctx.stroke();
      });
      ctx.fillStyle = css("--faint", "#64748b");
      ctx.font = "10px ui-monospace, monospace";
      ctx.textAlign = "center";
      ctx.fillText("LEFT", cxL, cy + 34);
      ctx.fillText("RIGHT", cxR, cy + 34);

      // baseline
      ctx.strokeStyle = css("--accent", "#22d3ee");
      ctx.beginPath();
      ctx.moveTo(cxL, cy - 34);
      ctx.lineTo(cxR, cy - 34);
      ctx.stroke();
      ctx.fillStyle = css("--accent", "#22d3ee");
      ctx.fillText(`b = ${(baseline * 100).toFixed(0)} cm`, w / 2, cy - 42);

      // scene point
      const py = cy - 92;
      const px = w / 2 + (depth - 2) * 16;
      ctx.fillStyle = css("--amber", "#fbbf24");
      ctx.beginPath();
      ctx.arc(px, py, 5, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillText(`Z = ${depth.toFixed(1)} m`, px, py - 12);

      // rays
      ctx.strokeStyle = "rgba(251,191,36,.6)";
      ctx.lineWidth = 1.1;
      [cxL, cxR].forEach((x) => {
        ctx.beginPath();
        ctx.moveTo(x, cy - 8);
        ctx.lineTo(px, py);
        ctx.stroke();
      });

      // image rows
      const rowY = 200;
      const rowW = 250;
      [cxL - rowW / 2, cxR - rowW / 2].forEach((x0, i) => {
        ctx.fillStyle = css("--bg-soft", "#0b1120");
        ctx.strokeStyle = css("--line-strong", "#475569");
        ctx.fillRect(x0, rowY, rowW, 26);
        ctx.strokeRect(x0, rowY, rowW, 26);
        const cx = x0 + rowW / 2 + (i === 0 ? -disp / 2 : disp / 2) * 1.6;
        ctx.fillStyle = css("--accent", "#22d3ee");
        ctx.beginPath();
        ctx.arc(clamp(cx, x0 + 6, x0 + rowW - 6), rowY + 13, 4, 0, Math.PI * 2);
        ctx.fill();
      });
      ctx.fillStyle = css("--faint", "#64748b");
      ctx.textAlign = "left";
      ctx.fillText("left retinal row", cxL - rowW / 2, rowY + 42);
      ctx.fillText("right retinal row", cxR - rowW / 2, rowY + 42);

      out.innerHTML =
        `disparity d = f·b/Z = <b>${disp.toFixed(1)} px</b> · depth Z = f·b/d<br>` +
        `uncertainty: ∂Z/∂d = −Z²/(f·b) → at this depth one pixel of disparity is <b>${((depth * depth) / (focal * baseline) * 1000).toFixed(1)} mm</b>`;
    }

    const box = el("div", { class: "viz" });
    box.append(cv, controls(
      slider({ label: "Baseline", min: 0.02, max: 0.6, step: 0.01, value: baseline, format: (v) => (v * 100).toFixed(0) + " cm", oninput: (v) => { baseline = v; render(); } }),
      slider({ label: "Depth Z", min: 0.5, max: 6, step: 0.1, value: depth, format: (v) => v.toFixed(1) + " m", oninput: (v) => { depth = v; render(); } }),
      slider({ label: "Focal (px)", min: 200, max: 1200, step: 10, value: focal, format: (v) => v, oninput: (v) => { focal = v; render(); } })
    ), out);
    stage.append(box);
    render();
  }

  /* ---------------------------------------------------------- 6. receptive field */

  function demoReceptive(stage) {
    let layers = 4, kernel = 3, stride = 1;
    const { cv, ctx, w, h } = makeCanvas(640, 250);
    const out = readout("");

    function compute() {
      let rf = 1, jump = 1, size = 64;
      const blocks = [];
      for (let i = 0; i < layers; i++) {
        rf += (kernel - 1) * jump;
        size = Math.floor((size - kernel) / stride) + 1;
        jump *= stride;
        blocks.push({ rf, jump, size });
        if (size < 1) break;
      }
      return { rf, jump, size: Math.max(size, 1), blocks };
    }

    function render() {
      const { rf, jump, size } = compute();
      const grid = 32;
      const cell = Math.min((w * 0.5 - 60) / grid, (h - 60) / grid);
      const ox = 30, oy = 30;
      ctx.clearRect(0, 0, w, h);

      // input grid
      for (let y = 0; y < grid; y++) {
        for (let x = 0; x < grid; x++) {
          ctx.fillStyle = (x + y) % 2 ? "rgba(148,163,184,.07)" : "rgba(148,163,184,.03)";
          ctx.fillRect(ox + x * cell, oy + y * cell, cell - 0.5, cell - 0.5);
        }
      }

      // receptive field patch centered
      const rfCells = Math.min(grid, rf);
      const startCell = Math.floor((grid - rfCells) / 2);
      ctx.strokeStyle = css("--accent", "#22d3ee");
      ctx.fillStyle = "rgba(34,211,238,.16)";
      ctx.lineWidth = 1.5;
      ctx.fillRect(ox + startCell * cell, oy + startCell * cell, rfCells * cell, rfCells * cell);
      ctx.strokeRect(ox + startCell * cell, oy + startCell * cell, rfCells * cell, rfCells * cell);

      // center pixel
      ctx.fillStyle = css("--amber", "#fbbf24");
      ctx.fillRect(ox + Math.floor(grid / 2) * cell, oy + Math.floor(grid / 2) * cell, cell, cell);

      // labels
      ctx.fillStyle = css("--faint", "#64748b");
      ctx.font = "10px ui-monospace, monospace";
      ctx.fillText(`input feature map (32×32 shown)`, ox, oy - 10);

      // formula column
      const tx = ox + grid * cell + 34;
      ctx.fillStyle = css("--text", "#e8eef8");
      ctx.font = "12px ui-monospace, monospace";
      ctx.fillText("RF ← RF + (k−1)·J", tx, 56);
      ctx.fillStyle = css("--muted", "#94a3b8");
      ctx.font = "11px ui-monospace, monospace";
      ctx.fillText(`layers   ${layers}`, tx, 86);
      ctx.fillText(`kernel   ${kernel}×${kernel}`, tx, 106);
      ctx.fillText(`stride   ${stride}`, tx, 126);
      ctx.fillStyle = css("--accent", "#22d3ee");
      ctx.fillText(`RF       ${rf}×${rf} px`, tx, 154);
      ctx.fillStyle = css("--muted", "#94a3b8");
      ctx.fillText(`jump     ${jump}`, tx, 174);
      ctx.fillText(`output   ${size}×${size}`, tx, 194);

      out.innerHTML =
        `After <b>${layers}</b> layers (k=${kernel}, s=${stride}) one output unit sees <b>${rf}×${rf}</b> input pixels, ` +
        `a stride-${jump} grid.<br>Cost of a deep stack: Naïve RF growth is linear in depth, but stride multiplies the jump, so resolution drops fast.`;
    }

    const box = el("div", { class: "viz" });
    box.append(cv, controls(
      slider({ label: "Layers", min: 1, max: 12, step: 1, value: layers, format: (v) => v, oninput: (v) => { layers = v; render(); } }),
      slider({ label: "Kernel", min: 1, max: 9, step: 2, value: kernel, format: (v) => v + "×" + v, oninput: (v) => { kernel = v; render(); } }),
      slider({ label: "Stride", min: 1, max: 3, step: 1, value: stride, format: (v) => v, oninput: (v) => { stride = v; render(); } })
    ), out);
    stage.append(box);
    render();
  }

  /* ------------------------------------------------------------------ 7. optimizer */

  function demoOptimizer(stage) {
    let lr = 0.12, momentum = 0.6, steps = 24;
    let useMomentum = true;
    const { cv, ctx, w, h } = makeCanvas(640, 300);
    const out = readout("");

    // elongated valley with a curved floor
    const loss = (x, y) => 0.9 * x * x + 6 * y * y + 0.4 * Math.sin(3 * x) * y + 0.15;

    function render() {
      ctx.clearRect(0, 0, w, h);
      const plot = { x: 26, y: 22, w: w - 52, h: h - 62 };
      const toScreen = (x, y) => [
        plot.x + ((x + 2.4) / 4.8) * plot.w,
        plot.y + ((y + 1.4) / 2.8) * plot.h,
      ];

      // contours
      for (let ring = 0; ring < 14; ring++) {
        const level = 0.06 * Math.pow(1.42, ring);
        ctx.beginPath();
        let started = false;
        for (let a = 0; a < Math.PI * 2; a += 0.02) {
          // sample the ellipse-ish contour numerically along the ray
          let r = 0.02;
          for (let k = 0; k < 60; k++) {
            const nx = Math.cos(a) * r, ny = Math.sin(a) * r;
            if (loss(nx, ny) > level) break;
            r += 0.012;
          }
          const [sx, sy] = toScreen(Math.cos(a) * r, Math.sin(a) * r);
          if (!started) { ctx.moveTo(sx, sy); started = true; }
          else ctx.lineTo(sx, sy);
        }
        ctx.closePath();
        ctx.strokeStyle = `rgba(148,163,184,${0.30 - ring * 0.017})`;
        ctx.lineWidth = 1;
        ctx.stroke();
      }

      // gradient descent
      let x = -1.9, y = 0.85, vx = 0, vy = 0;
      const path = [[x, y]];
      for (let i = 0; i < steps; i++) {
        const eps = 1e-3;
        const gx = (loss(x + eps, y) - loss(x - eps, y)) / (2 * eps);
        const gy = (loss(x, y + eps) - loss(x, y - eps)) / (2 * eps);
        if (useMomentum) {
          vx = momentum * vx - lr * gx;
          vy = momentum * vy - lr * gy;
          x += vx;
          y += vy;
        } else {
          x -= lr * gx;
          y -= lr * gy;
        }
        x = clamp(x, -2.2, 2.2);
        y = clamp(y, -1.2, 1.2);
        path.push([x, y]);
        if (!isFinite(x) || !isFinite(y)) break;
      }

      ctx.strokeStyle = css("--accent", "#22d3ee");
      ctx.lineWidth = 1.8;
      ctx.beginPath();
      path.forEach(([px, py], i) => {
        const [sx, sy] = toScreen(px, py);
        i ? ctx.lineTo(sx, sy) : ctx.moveTo(sx, sy);
      });
      ctx.stroke();
      path.forEach(([px, py], i) => {
        const [sx, sy] = toScreen(px, py);
        ctx.fillStyle = i === path.length - 1 ? css("--amber", "#fbbf24") : `rgba(34,211,238,${0.25 + 0.6 * (i / path.length)})`;
        ctx.beginPath();
        ctx.arc(sx, sy, i === path.length - 1 ? 4.5 : 2.2, 0, Math.PI * 2);
        ctx.fill();
      });

      ctx.fillStyle = css("--faint", "#64748b");
      ctx.font = "10px ui-monospace, monospace";
      ctx.fillText("contours of L(θ) · θ = (x, y)", 26, h - 16);
      out.innerHTML =
        `final loss <b>${loss(x, y).toFixed(4)}</b> at (${x.toFixed(2)}, ${y.toFixed(2)}) · ${steps} steps<br>` +
        (lr > 0.5 ? "⚠ steps are large: the update overshoots the narrow axis and oscillates." :
          useMomentum ? "momentum accumulates velocity along consistent directions, damping zig-zag." :
            "plain gradient descent zig-zags across the valley because curvature is anisotropic.");
    }

    const toggle = el("div", { class: "viz__chips" });
    const plain = el("button", { class: "viz__chip", type: "button" }, "SGD");
    const mom = el("button", { class: "viz__chip is-active", type: "button" }, "Momentum");
    [[plain, false], [mom, true]].forEach(([btn, flag]) => {
      btn.addEventListener("click", () => {
        useMomentum = flag;
        plain.classList.toggle("is-active", !flag);
        mom.classList.toggle("is-active", flag);
        render();
      });
      toggle.append(btn);
    });

    const box = el("div", { class: "viz" });
    box.append(cv, toggle, controls(
      slider({ label: "Learning rate", min: 0.01, max: 0.8, step: 0.01, value: lr, format: (v) => v.toFixed(2), oninput: (v) => { lr = v; render(); } }),
      slider({ label: "Momentum", min: 0, max: 0.95, step: 0.05, value: momentum, format: (v) => v.toFixed(2), oninput: (v) => { momentum = v; render(); } }),
      slider({ label: "Steps", min: 1, max: 60, step: 1, value: steps, format: (v) => v, oninput: (v) => { steps = v; render(); } })
    ), out);
    stage.append(box);
    render();
  }

  /* ----------------------------------------------------------------- 8. diffusion */

  function demoDiffusion(stage) {
    let t = 300;
    const W = 64, H = 48;
    const clean = scene(W, H, 6);
    const noise = new Float32Array(W * H * 3);
    let seed = 7;
    const rnd = () => {
      seed = (seed * 1664525 + 1013904223) % 4294967296;
      return seed / 4294967296;
    };
    for (let i = 0; i < noise.length; i++) {
      // Box–Muller for Gaussian noise
      const u1 = Math.max(rnd(), 1e-6), u2 = rnd();
      noise[i] = Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2) * 127.5;
    }

    const { cv, ctx, w, h } = makeCanvas(640, 250);
    const out = readout("");

    // cosine schedule: alpha_bar(t)
    const abar = (step) => {
      const s = 0.008;
      const f = (x) => Math.cos(((x + s) / (1 + s)) * (Math.PI / 2)) ** 2;
      return f(step / 1000) / f(0);
    };

    function render() {
      const a = abar(t);
      const px = new Float32Array(W * H * 3);
      for (let i = 0; i < px.length; i++) {
        px[i] = clamp(Math.sqrt(a) * clean[i] + Math.sqrt(1 - a) * noise[i], 0, 255);
      }
      ctx.clearRect(0, 0, w, h);
      const pad = 16, top = 32;
      const cw = (w - pad * 3) / 2;
      const ch = Math.min(h - top - 26, cw * 0.72);
      drawRGB(ctx, clean, W, H, { x: pad, y: top, cw, ch });
      drawRGB(ctx, px, W, H, { x: pad * 2 + cw, y: top, cw, ch });

      ctx.fillStyle = css("--faint", "#64748b");
      ctx.font = "10px ui-monospace, monospace";
      ctx.fillText("x₀ (clean)", pad, 22);
      ctx.fillText(`x_t at t = ${t}`, pad * 2 + cw, 22);

      // noise bar
      const barY = top + ch + 14;
      ctx.fillStyle = "rgba(148,163,184,.15)";
      ctx.fillRect(pad, barY, w - pad * 2, 6);
      ctx.fillStyle = css("--accent", "#22d3ee");
      ctx.fillRect(pad, barY, (w - pad * 2) * (t / 1000), 6);

      out.innerHTML =
        `x<sub>t</sub> = √ᾱ<sub>t</sub>·x₀ + √(1−ᾱ<sub>t</sub>)·ε · ᾱ = <b>${a.toFixed(3)}</b> → signal ${(Math.sqrt(a) * 100).toFixed(0)}%, noise ${(Math.sqrt(1 - a) * 100).toFixed(0)}%<br>` +
        (t > 850 ? "Nearly pure noise: the reverse process must recover structure from the prior alone." : "The forward process is fixed and Markovian; only the reverse model is learned.");
    }

    const box = el("div", { class: "viz" });
    box.append(cv, controls(
      slider({ label: "Timestep t", min: 0, max: 1000, step: 10, value: t, format: (v) => v, oninput: (v) => { t = v; render(); } })
    ), out);
    stage.append(box);
    render();
  }

  /* ----------------------------------------------------------------------- 9. IoU */

  function demoIoU(stage) {
    let x = 96, y = 60, pw = 170, ph = 130;
    let thresh = 0.5;
    const { cv, ctx, w, h } = makeCanvas(640, 260);
    const out = readout("");
    const gt = { x: 70, y: 52, w: 180, h: 140 };

    function render() {
      const ix = Math.max(gt.x, x);
      const iy = Math.max(gt.y, y);
      const iw = Math.max(0, Math.min(gt.x + gt.w, x + pw) - ix);
      const ih = Math.max(0, Math.min(gt.y + gt.h, y + ph) - iy);
      const inter = iw * ih;
      const union = gt.w * gt.h + pw * ph - inter;
      const iou = union > 0 ? inter / union : 0;
      const tp = iou >= thresh;

      ctx.clearRect(0, 0, w, h);
      drawRGB(ctx, scene(80, 52, 8), 80, 52, { x: 0, y: 0, cw: w, ch: h });
      ctx.fillStyle = "rgba(3,7,18,.45)";
      ctx.fillRect(0, 0, w, h);

      ctx.setLineDash([]);
      ctx.strokeStyle = css("--green", "#34d399");
      ctx.lineWidth = 2;
      ctx.strokeRect(gt.x, gt.y, gt.w, gt.h);
      ctx.fillStyle = css("--green", "#34d399");
      ctx.font = "10px ui-monospace, monospace";
      ctx.fillText("ground truth", gt.x, gt.y - 7);

      ctx.strokeStyle = tp ? css("--accent", "#22d3ee") : css("--red", "#fb7185");
      ctx.lineWidth = 2;
      ctx.strokeRect(x, y, pw, ph);
      ctx.fillStyle = tp ? css("--accent", "#22d3ee") : css("--red", "#fb7185");
      ctx.fillText(tp ? "prediction · TP" : "prediction · FP", x, y - 7);

      if (iw > 0 && ih > 0) {
        ctx.fillStyle = "rgba(34,211,238,.22)";
        ctx.fillRect(ix, iy, iw, ih);
        ctx.strokeStyle = css("--accent", "#22d3ee");
        ctx.setLineDash([3, 3]);
        ctx.strokeRect(ix, iy, iw, ih);
        ctx.setLineDash([]);
      }

      out.innerHTML =
        `IoU = |A∩B| / |A∪B| = ${inter.toLocaleString()} / ${union.toLocaleString()} = <b>${iou.toFixed(3)}</b> ` +
        `→ ${tp ? "detection kept at IoU ≥ " + thresh : "discarded at IoU ≥ " + thresh}<br>` +
        `COCO averages AP over IoU 0.50:0.05:0.95; a single confident but loose box scores poorly there.`;
    }

    const box = el("div", { class: "viz" });
    box.append(cv, controls(
      slider({ label: "Box x", min: 0, max: 380, step: 2, value: x, format: (v) => v + "px", oninput: (v) => { x = v; render(); } }),
      slider({ label: "Box y", min: 0, max: 180, step: 2, value: y, format: (v) => v + "px", oninput: (v) => { y = v; render(); } }),
      slider({ label: "Width", min: 40, max: 260, step: 2, value: pw, format: (v) => v, oninput: (v) => { pw = v; render(); } }),
      slider({ label: "Height", min: 40, max: 200, step: 2, value: ph, format: (v) => v, oninput: (v) => { ph = v; render(); } }),
      slider({ label: "IoU threshold", min: 0.3, max: 0.95, step: 0.05, value: thresh, format: (v) => v.toFixed(2), oninput: (v) => { thresh = v; render(); } })
    ), out);
    stage.append(box);
    render();
  }

  /* -------------------------------------------------------------------- registry */

  const DEMOS = {
    convolution: demoConvolution,
    histogram: demoHistogram,
    edges: demoEdges,
    pinhole: demoPinhole,
    stereo: demoStereo,
    receptive: demoReceptive,
    optimizer: demoOptimizer,
    diffusion: demoDiffusion,
    iou: demoIoU,
  };

  function mount() {
    document.querySelectorAll("[data-demo]").forEach((figure) => {
      const id = figure.dataset.demo;
      const stage = figure.querySelector(".demo__stage");
      const fn = DEMOS[id];
      if (!stage || !fn) {
        if (stage) stage.innerHTML = '<p class="muted">This lab is not available in the static build.</p>';
        return;
      }
      try {
        fn(stage);
      } catch (error) {
        stage.innerHTML = '<p class="muted">Lab failed to render: ' + String(error.message || error) + "</p>";
      }
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", mount);
  else mount();
})();
