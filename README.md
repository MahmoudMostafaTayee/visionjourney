# Vision Journey

**A free, deep computer vision curriculum — from the camera obscura to foundation models.**

Vision Journey is a learning platform in the spirit of [Linux Journey](https://labex.io/linuxjourney): structured lessons, a clean reading layout, short checks as you go, and a map that takes you from absolute foundations to research practice. It differs in two ways that matter for vision:

- **Real architectures, not diagrams.** The Model Lab ships ONNX models exported from PyTorch and renders their computation graphs with true tensor shapes. Click a node to see its operation, output shape and parameter count — or open the same file in [Netron](https://netron.app) for attributes and weights.
- **Interactive labs instead of static figures.** Convolution kernels, tonal histograms, Canny thresholds, pinhole projection, stereo disparity, receptive fields, optimisation paths, diffusion timesteps and IoU are all manipulable in the browser.

```bash
python3 tools/build.py            # build the static site into site/
python3 -m http.server -d site 8000
# open http://localhost:8000
```

No Node, npm or bundler required. The build needs Python 3.10+, PyYAML, and — only to regenerate the models — PyTorch, torchvision and onnx.

---

## The curriculum

Three levels, thirteen courses, thirty-nine lessons — about 27,000 words of technical writing. Each lesson is a focused, self-contained piece (typically 600–800 words) with primary-source links, worked numbers and three to five checks.

### Level I — Foundations

| # | Course | Lessons |
|---|--------|---------|
| 1 | **Vision History** | Before the Camera · The Birth of Computer Vision · The Deep-Learning Earthquake |
| 2 | **Image Formation & Digital Images** | Pinhole and Projection · Sensors, Colour and Radiometry · The Anatomy of a Digital Image |
| 3 | **Mathematics for Vision** | Tensors and Linear Algebra · Calculus and Automatic Differentiation · Optimisation and Gradient Descent |
| 4 | **Classical Image Processing** | Convolution and Filtering · Edges and Gradients · Morphology and Histograms |
| 5 | **Features, Matching & Geometry** | Corners and Descriptors · Matching and Robust Estimation · Camera Geometry and Stereo |

### Level II — Deep Vision

| # | Course | Lessons |
|---|--------|---------|
| 6 | **Neural Networks from Scratch** | Perceptrons and Multilayer Networks · Backpropagation by Hand · Training Dynamics |
| 7 | **Convolutional Networks** | Anatomy of a Convolutional Network · Landmark Architectures · Receptive Fields and Architectural Bias |
| 8 | **Recognition** | Image Classification · Object Detection · Semantic and Instance Segmentation |
| 9 | **Attention & Self-Supervision** | Attention and the Vision Transformer · Self-Supervised Learning · Vision-Language Models |
| 10 | **Generative & 3D Vision** | VAEs and GANs · Diffusion Models · Neural Fields and 3D Vision |

### Level III — Research Frontier

| # | Course | Lessons |
|---|--------|---------|
| 11 | **Research Practice** | Reading Research Papers · Reproducible Experiments · Benchmarking and Ablation |
| 12 | **Model Inspection & Interpretability** | Computation Graphs and Netron · Interpretability · Efficiency and Deployment |
| 13 | **Robustness, Ethics & Open Problems** | Adversarial Robustness · Privacy, Fairness and Ethics · Open Problems and How to Contribute |

---

## The Model Lab

Five architectures are exported from real PyTorch modules, deliberately small so the repository stays light:

| Model | Task | Parameters | What to look for |
|-------|------|-----------|------------------|
| Demo CNN | 10-class, 1×28×28 | 52.1K | The smallest complete vision graph: conv → pool → conv → pool → fc |
| ResNet-Mini | Residual, 3×64×64 | 38.0K | Identity shortcuts as parallel graph edges, and Add nodes |
| Tiny ViT | Patch transformer, 3×32×32 | 21.2K | QKV projection, head reshape, MatMul → Softmax → MatMul |
| U-Net Mini | Segmentation, 3×64×64 | 117.4K | Encoder/decoder skips via Concat across the bottleneck |
| Mobile Inverted Residual | Efficient, 3×64×64 | 19.0K | Depthwise convolution where `group == channels` |

Every model has:
- a real `.onnx` file in `models/` that can be dragged into Netron;
- a pre-computed graph in `models/graphs/*.json` with per-node shapes and parameter counts;
- an entry in `models/catalog.json` shown on the Model Lab page.

The explorer supports zoom, pan, horizontal/vertical layout, collapsing repeated blocks, and a node inspector. The Netron iframe and deep links use `netron.app`, so they require network access, and a Netron deep link only works when this site is itself served over **HTTPS** — `netron.app` is HTTPS and the browser blocks it from fetching a model over plain HTTP. On a local `http://localhost` server the page therefore tells you to download the `.onnx` and drag it onto the Netron panel instead. The offline explorer always works.

To regenerate the models after changing `tools/export_models.py`:

```bash
python3 tools/export_models.py
python3 tools/build.py
```

---

## Repository layout

```text
visionjourney/
├── site.yml                     # site metadata, levels, timeline
├── courses/<course-id>.yml      # course metadata (title, description, FAQs, SEO)
├── lessons/en/<course>/<lesson>.md
├── models/
│   ├── *.onnx                   # exported, inspectable models
│   ├── graphs/*.json            # shapes + edges for the offline explorer
│   └── catalog.json
├── engine/                      # content engine — knows nothing about vision
│   ├── blocks.py                # split rendered lesson HTML into blocks
│   └── tutorial.py              # the tutorial page presenter (steps + controls)
├── tools/
│   ├── build.py                 # static site baker: content + engine → site/
│   └── export_models.py         # PyTorch → ONNX → graph JSON
├── assets/css/style.css
├── assets/js/{app,viz,graph}.js
└── site/                        # generated output (not source)
```

The content schema deliberately follows Linux Journey's conventions: `courses/<id>.yml`, `lessons/<lang>/<course>/<lesson>.md`, YAML front matter, and `:::single-choice` checks. A lesson's path must agree with its `lesson_id`, `course_id` and `lang`.

## Engine and content

Content and presentation are separate. `lessons/` and `courses/` hold only writing — markdown, front matter and checks — and never mention layout. `engine/` holds the reader:

- `engine/blocks.py` splits rendered lesson HTML into top-level blocks (paragraph, heading, list, code, figure, callout, check).
- `engine/tutorial.py` is the tutorial page presenter. `present_tutorial(content, finish_href=…, finish_label=…)` groups the blocks into steps — one paragraph each, with its heading and any list, code, figure or check that belongs to it — and returns the step markup plus the controls. It decides nothing about the site: the caller supplies where the lesson ends.
- `tools/build.py` is the baker. It loads content, renders markdown, hands the HTML to the presenter, and writes `site/`.

Adding a new presentation module (a quiz-only drill, a printable view) means adding a file under `engine/`; it never requires touching lesson text. Adding lessons never requires touching the engine.

## Lesson directives

Beyond standard Markdown, four directives are supported:

```markdown
:::single-choice{#component-id} The question text goes on the same line.

::option[A plausible but wrong answer]{#option-id explanation="Why it is wrong."}
::option[The correct answer]{#option-id .correct explanation="Why it is right."}
::option[Another plausible answer]{#option-id explanation="Why it is wrong."}
:::

:::demo{id="convolution"} Optional title
Markdown body explaining what to manipulate.
:::

:::model{src="resnet-mini"} Optional title
:::

:::callout{type="warning" title="Short title"}
Markdown body.
:::
```

Available demo ids: `convolution`, `histogram`, `edges`, `pinhole`, `stereo`, `receptive`, `optimizer`, `diffusion`, `iou`.

Available model ids: `demo-cnn`, `resnet-mini`, `vit-tiny`, `unet-mini`, `mobilenet-block`.

## Features

- **Guided path** at `path.html`: all 39 lessons in one numbered sequence with a progress bar and a continue button that jumps to the next unfinished lesson. Lesson pages link to the previous and next lesson *across course boundaries*, so you never have to go back to a menu to keep going.
- **Paragraph-by-paragraph lessons, Linux Journey style**: the engine presents one paragraph at a time (with whatever heading, list, code, figure or check belongs to it), a centred **Continue** button below it, and a progress meter. When a step ends in a check, Continue is disabled until the check is answered; a wrong option is eliminated so you can try again. The outline jumps to the step holding the heading, the footer pager appears only at the end, and without JavaScript the whole lesson renders as a single page.
- **Wide three-column lesson layout**: course navigation, a generously sized prose column, and an on-this-page outline that collapses below 1120px.
- **Progress tracking** in `localStorage`: completed lessons and solved checks persist per browser.
- **Client-side search** over lesson text, courses and snippets, with keyboard navigation (`⌘K` or `/`).
- **Calculation blocks** rendered with KaTeX. Math falls back to readable plain text if the CDN is unavailable.
- **Light and dark themes**, responsive down to mobile, reduced-motion support.
- **Generated course art** — deterministic SVG, no binary image assets or licensing questions.
- **Accessible fundamentals**: skip link, semantic landmarks, focusable quiz buttons, status announcements for feedback.

## Verification

```bash
python3 tools/build.py                     # builds 39 lessons, 13 courses
python3 - <<'PY'
import json, pathlib
files = list(pathlib.Path("site").rglob("*.html"))
print(len(files), "pages")
json.load(open("site/search-index.json"))
json.load(open("site/models/catalog.json"))
PY
```

The generator prints the lesson and course count and the output directory. Lessons whose front matter cannot be parsed are skipped rather than failing the whole build, so compare the printed lesson total against `ls lessons/en/*/*.md` after structural edits.

## Content provenance and attribution

This curriculum was authored for this repository. Its *structure* is inspired by Linux Journey (LabEx), and the curated resource list draws on several public collections, credited in [RESOURCES.md](RESOURCES.md):

- [developer-roadmap](https://github.com/kamranahmedse/developer-roadmap) — ML, MLOps and AI red-teaming roadmaps used to cross-check topic coverage.
- [free-programming-books](https://github.com/EbookFoundation/free-programming-books) — free books and courses.
- [build-your-own-x](https://github.com/codecrafters-io/build-your-own-x) — from-scratch implementations.
- [awesome](https://github.com/sindresorhus/awesome) and the [awesome-computer-vision](https://github.com/jbhuang0604/awesome-computer-vision) list.
- [coding-interview-university](https://github.com/jwasham/coding-interview-university) — mathematical and algorithmic foundations.

Links point to their original authors and are not mirrored here.

## License

Content is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Code is MIT. Model files are generated by `tools/export_models.py` from standard architectural definitions and carry the same MIT licence.

This project is independent and is not affiliated with Linux Journey or LabEx.
