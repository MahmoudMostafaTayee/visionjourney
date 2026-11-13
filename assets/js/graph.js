/* Vision Journey — ONNX computation-graph explorer (Netron-style, offline). */
(() => {
  "use strict";

  const root = document.body.dataset.root || "";
  const SVG_NS = "http://www.w3.org/2000/svg";

  const OP_KIND = {
    Conv: "conv", ConvTranspose: "conv", QLinearConv: "conv",
    BatchNormalization: "norm", LayerNormalization: "norm", GroupNormalization: "norm", InstanceNormalization: "norm",
    Relu: "act", LeakyRelu: "act", Gelu: "act", Sigmoid: "act", Tanh: "act", Softmax: "act", HardSwish: "act", Erf: "act", PRelu: "act", Clip: "act",
    MaxPool: "pool", AveragePool: "pool", GlobalAveragePool: "pool", Reshape: "pool", Flatten: "pool", Concat: "pool", Split: "pool", Transpose: "pool", Squeeze: "pool", Unsqueeze: "pool", Slice: "pool", Gather: "pool",
    Gemm: "linear", MatMul: "linear", Add: "linear",
  };

  const KIND_COLOR = {
    conv: "var(--c-conv)",
    norm: "var(--c-norm)",
    act: "var(--c-act)",
    pool: "var(--c-pool)",
    linear: "var(--c-linear)",
    other: "#94a3b8",
  };

  const svgEl = (tag, attrs = {}) => {
    const node = document.createElementNS(SVG_NS, tag);
    for (const [k, v] of Object.entries(attrs)) node.setAttribute(k, v);
    return node;
  };

  const shapeText = (shape) => (shape && shape.length ? shape.join("×") : "");
  const fmt = (n) => {
    if (n == null) return "—";
    if (n >= 1e9) return (n / 1e9).toFixed(1) + "G";
    if (n >= 1e6) return (n / 1e6).toFixed(1) + "M";
    if (n >= 1e3) return (n / 1e3).toFixed(1) + "K";
    return String(n);
  };

  /* --------------------------------------------------------------- layout */

  function computeDepths(nodes, edges) {
    const incoming = nodes.map(() => []);
    edges.forEach(([a, b]) => incoming[b]?.push(a));
    const depth = new Array(nodes.length).fill(0);
    // Kahn-style relaxation; bounded to be safe on malformed graphs.
    for (let pass = 0; pass < nodes.length + 1; pass++) {
      let changed = false;
      edges.forEach(([a, b]) => {
        if (depth[b] < depth[a] + 1) {
          depth[b] = depth[a] + 1;
          changed = true;
        }
      });
      if (!changed) break;
    }
    void incoming;
    return depth;
  }

  function collapse(nodes, edges) {
    if (!nodes.some((n) => n.stage)) return { nodes, edges, groups: null };
    const order = [];
    const map = new Map();
    nodes.forEach((n, i) => {
      const key = n.stage || n.op;
      if (!map.has(key)) {
        map.set(key, { id: order.length, name: key, count: 0, ops: [], first: i, last: i, out: n.out });
        order.push(map.get(key));
      }
      const g = map.get(key);
      g.count += 1;
      g.ops.push(n.op);
      g.last = i;
      g.out = n.out;
    });
    const grouped = order.map((g) => {
      const kinds = {};
      g.ops.forEach((op) => {
        const k = OP_KIND[op] || "other";
        kinds[k] = (kinds[k] || 0) + 1;
      });
      const kind = Object.keys(kinds).sort((a, b) => kinds[b] - kinds[a])[0] || "other";
      return {
        op: g.name,
        name: g.name,
        kind,
        collapsed: g.count,
        out: g.out,
        stage: g.name,
        params: nodes.slice(g.first, g.last + 1).reduce((a, n) => a + (n.params || 0), 0),
        outShape: g.out,
        ops: g.ops,
      };
    });
    const idxOfNode = new Map();
    nodes.forEach((n, i) => {
      const key = n.stage || n.op;
      idxOfNode.set(i, order.findIndex((g) => g.name === key));
    });
    const seen = new Set();
    const newEdges = [];
    edges.forEach(([a, b]) => {
      const ga = idxOfNode.get(a), gb = idxOfNode.get(b);
      if (ga == null || gb == null || ga === gb) return;
      const key = `${ga}-${gb}`;
      if (seen.has(key)) return;
      seen.add(key);
      newEdges.push([ga, gb]);
    });
    return { nodes: grouped, edges: newEdges, groups: true };
  }

  /* ----------------------------------------------------------------- render */

  function createViewer(container, options = {}) {
    let graph = null;
    let layoutMode = "horizontal";
    let detail = "all";
    let scale = 1, tx = 0, ty = 0;
    let selected = -1;

    const svg = svgEl("svg", { viewBox: "0 0 100 100", preserveAspectRatio: "xMidYMid meet" });
    const viewport = svgEl("g");
    svg.append(viewport);
    container.innerHTML = "";
    container.append(svg);

    const inspector = options.inspector || null;

    function draw() {
      const model = detail === "blocks" ? collapse(graph.nodes, graph.edges) : { nodes: graph.nodes, edges: graph.edges };
      const nodes = model.nodes;
      const edges = model.edges;
      const depths = computeDepths(nodes, edges);
      const maxDepth = Math.max(...depths, 0);

      const boxW = layoutMode === "horizontal" ? 156 : 150;
      const boxH = layoutMode === "horizontal" ? 46 : 44;
      const gapMain = layoutMode === "horizontal" ? 74 : 62;
      const gapCross = layoutMode === "horizontal" ? 58 : 70;

      const columns = Array.from({ length: maxDepth + 1 }, () => []);
      depths.forEach((d, i) => columns[d].push(i));

      const pos = new Map();
      let maxCross = 0;
      columns.forEach((col, ci) => {
        maxCross = Math.max(maxCross, col.length);
        col.forEach((nodeIndex, ri) => {
          const offset = (col.length - 1) / 2;
          const cross = (ri - offset) * (layoutMode === "horizontal" ? boxH + 12 : boxW + 16) + 0;
          if (layoutMode === "horizontal") {
            pos.set(nodeIndex, { x: ci * (boxW + gapMain), y: cross - boxH / 2 });
          } else {
            pos.set(nodeIndex, { x: cross - boxW / 2, y: ci * (boxH + gapCross) });
          }
        });
      });
      void gapCross;

      viewport.innerHTML = "";

      // edges first
      edges.forEach(([a, b]) => {
        const pa = pos.get(a), pb = pos.get(b);
        if (!pa || !pb) return;
        let d;
        if (layoutMode === "horizontal") {
          const x1 = pa.x + boxW, y1 = pa.y + boxH / 2;
          const x2 = pb.x, y2 = pb.y + boxH / 2;
          const dx = Math.max(24, (x2 - x1) / 2);
          d = `M${x1},${y1} C${x1 + dx},${y1} ${x2 - dx},${y2} ${x2},${y2}`;
        } else {
          const x1 = pa.x + boxW / 2, y1 = pa.y + boxH;
          const x2 = pb.x + boxW / 2, y2 = pb.y;
          const dy = Math.max(20, (y2 - y1) / 2);
          d = `M${x1},${y1} C${x1},${y1 + dy} ${x2},${y2 - dy} ${x2},${y2}`;
        }
        const path = svgEl("path", { d, class: "gedge" });
        if (selected >= 0 && (a === selected || b === selected)) path.classList.add("gedge--emph");
        viewport.append(path);
      });

      // nodes
      nodes.forEach((node, i) => {
        const p = pos.get(i);
        if (!p) return;
        const kind = node.kind || OP_KIND[node.op] || "other";
        const g = svgEl("g", { class: "gnode", transform: `translate(${p.x},${p.y})` });
        const rect = svgEl("rect", {
          width: boxW,
          height: boxH,
          rx: 8,
          fill: KIND_COLOR[kind],
          stroke: i === selected ? "var(--text)" : "rgba(0,0,0,.25)",
          "stroke-width": i === selected ? 2 : 1,
        });
        g.append(rect);

        const label = node.collapsed ? `${node.name} ×${node.collapsed}` : node.op;
        const name = svgEl("text", { x: 10, y: 19, class: "gnode__name" });
        name.textContent = label.length > 20 ? label.slice(0, 19) + "…" : label;
        g.append(name);

        const shape = svgEl("text", { x: 10, y: 34, class: "gnode__shape" });
        shape.textContent = shapeText(node.out) || (node.collapsed ? `${node.count} layers` : "");
        g.append(shape);

        g.addEventListener("click", (event) => {
          event.stopPropagation();
          selected = i;
          draw();
          showNode(node);
        });
        viewport.append(g);
      });

      // fit
      const totalW = maxDepth * (boxW + gapMain) + boxW;
      const totalH = maxCross * (boxH + 14) + boxH;
      void totalW;
      void totalH;
      if (options.fit !== false) fit();
    }

    function fit() {
      const bbox = viewport.getBBox();
      if (!bbox.width || !bbox.height) return;
      const rect = container.getBoundingClientRect();
      const pad = 34;
      scale = Math.min((rect.width - pad * 2) / bbox.width, (rect.height - pad * 2) / bbox.height, 1.15);
      scale = Math.max(scale, 0.12);
      tx = rect.width / 2 - (bbox.x + bbox.width / 2) * scale;
      ty = rect.height / 2 - (bbox.y + bbox.height / 2) * scale;
      apply();
    }

    function apply() {
      viewport.setAttribute("transform", `translate(${tx},${ty}) scale(${scale})`);
    }

    function showNode(node) {
      if (!inspector) return;
      const attrs = node.attrs && Object.keys(node.attrs).length
        ? Object.entries(node.attrs).map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(", ") : v}`).join("<br>")
        : "—";
      inspector.innerHTML =
        `<p class="panel__title">Node inspector</p>` +
        `<dl>` +
        `<dt>op</dt><dd>${escape(node.op || node.name)}</dd>` +
        `<dt>name</dt><dd>${escape(node.name || "—")}</dd>` +
        `<dt>output shape</dt><dd>${shapeText(node.out || node.outShape) || "—"}</dd>` +
        `<dt>params</dt><dd>${fmt(node.params)}</dd>` +
        (node.collapsed ? `<dt>layers</dt><dd>${node.collapsed} (${escape((node.ops || []).slice(0, 6).join(", "))}${(node.ops || []).length > 6 ? "…" : ""})</dd>` : "") +
        `<dt>attributes</dt><dd>${attrs}</dd>` +
        `</dl>`;
    }

    function escape(text) {
      return String(text == null ? "—" : text).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
    }

    /* interaction: wheel zoom + drag pan */
    let dragging = false, lastX = 0, lastY = 0;
    svg.addEventListener("wheel", (event) => {
      event.preventDefault();
      const rect = container.getBoundingClientRect();
      const mx = event.clientX - rect.left, my = event.clientY - rect.top;
      const factor = event.deltaY < 0 ? 1.12 : 1 / 1.12;
      const next = Math.min(3, Math.max(0.12, scale * factor));
      tx = mx - ((mx - tx) / scale) * next;
      ty = my - ((my - ty) / scale) * next;
      scale = next;
      apply();
    }, { passive: false });

    svg.addEventListener("pointerdown", (event) => {
      dragging = true;
      lastX = event.clientX;
      lastY = event.clientY;
      svg.setPointerCapture(event.pointerId);
    });
    svg.addEventListener("pointermove", (event) => {
      if (!dragging) return;
      tx += event.clientX - lastX;
      ty += event.clientY - lastY;
      lastX = event.clientX;
      lastY = event.clientY;
      apply();
    });
    svg.addEventListener("pointerup", () => (dragging = false));
    svg.addEventListener("pointercancel", () => (dragging = false));
    svg.addEventListener("click", () => { selected = -1; draw(); });

    return {
      async load(id) {
        container.innerHTML = '<div class="lab__empty">Loading graph…</div>';
        try {
          const res = await fetch(`${root}models/graphs/${id}.json`);
          graph = await res.json();
        } catch (error) {
          container.innerHTML = '<div class="lab__empty">Could not load the graph for ' + escape(id) + ".</div>";
          return;
        }
        container.innerHTML = "";
        container.append(svg);
        selected = -1;
        draw();
      },
      setLayout(mode) { layoutMode = mode; if (graph) draw(); },
      setDetail(mode) { detail = mode; if (graph) draw(); },
      fit() { if (graph) fit(); },
      current() { return graph; },
    };
  }

  /* ---------------------------------------------------------------- wiring */

  function netronUrl(file) {
    // netron.app is served over HTTPS, so it cannot fetch a model from a plain-HTTP
    // origin: the browser blocks it as mixed content. Only build a deep link when
    // this page is itself served over HTTPS; otherwise we explain the drag-and-drop route.
    if (location.protocol !== "https:") return null;
    const absolute = new URL(`${root}models/${file}`, location.href).href;
    return `https://netron.app/?url=${encodeURIComponent(absolute)}`;
  }

  let netronNoticeShown = false;
  function netronInsecureNotice() {
    if (netronNoticeShown) return;
    netronNoticeShown = true;
    const note = document.querySelector("[data-netron-note]");
    if (!note) return;
    note.textContent =
      `Netron is served over HTTPS, so it cannot load a model from ${location.origin} ` +
      "(mixed content). Download the .onnx file and drag it onto the Netron panel, or use the offline explorer above.";
    note.classList.add("netron__note");
  }

  const labStage = document.querySelector("[data-graph-stage]");
  const inspector = document.querySelector("[data-graph-inspect]");

  async function bootLab() {
    if (!labStage) return;
    const viewer = createViewer(labStage, { inspector });
    labStage.viewer = viewer;

    document.querySelectorAll("[data-model-pick]").forEach((card) => {
      card.addEventListener("click", async () => {
        document.querySelectorAll("[data-model-pick]").forEach((c) => c.classList.remove("is-active"));
        card.classList.add("is-active");
        await viewer.load(card.dataset.modelPick);
        const model = viewer.current();
        const frame = document.querySelector("[data-netron]");
        if (frame && model && model.file) {
          const url = netronUrl(model.file);
          if (url) frame.src = url;
          else netronInsecureNotice();
        }
      });
    });

    document.querySelector("[data-graph-layout]")?.addEventListener("change", (e) => viewer.setLayout(e.target.value));
    document.querySelector("[data-graph-detail]")?.addEventListener("change", (e) => viewer.setDetail(e.target.value));
    document.querySelector("[data-graph-fit]")?.addEventListener("click", () => viewer.fit());

    document.querySelectorAll("[data-netron-open]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const url = netronUrl(btn.dataset.netronOpen);
        if (!url) {
          netronInsecureNotice();
          return;
        }
        const frame = document.querySelector("[data-netron]");
        if (frame) frame.src = url;
        window.open(url, "_blank", "noopener");
      });
    });

    const first = document.querySelector("[data-model-pick]");
    if (first) first.click();
  }

  function bootEmbeds() {
    document.querySelectorAll("[data-model]").forEach((figure) => {
      const stage = figure.querySelector(".graph-embed__stage");
      if (!stage) return;
      const viewer = createViewer(stage, { fit: true });
      viewer.load(figure.dataset.model);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => { bootLab(); bootEmbeds(); });
  } else {
    bootLab();
    bootEmbeds();
  }
})();
