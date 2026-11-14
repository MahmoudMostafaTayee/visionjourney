# Madarik — مدارك

**An open learning platform: independent curricula, one engine.**

The platform is called **Madarik** (مدارِك, “perception, faculties of understanding”). It publishes whole curricula, each written as content only — its own courses, lessons and checks, its own front page and guided path. The first is **Vision Journey**, a free, deep computer vision curriculum from the camera obscura to foundation models. The platform name lives in one line of `topics.yml`; the curriculum name lives in `content/vision/site.yml`.

Vision Journey is built for study rather than browsing: structured lessons, a clean reading layout, short checks as you go, and a map that takes you from absolute foundations to research practice. Two things make it different from a textbook:

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
- a real `.onnx` file in the topic's `models/` folder that can be dragged into Netron;
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
├── topics.yml                   # the curricula this site publishes
├── content/<topic>/              # content only — no layout, no code
│   ├── site.yml                  # title, levels, nav, hero copy, features
│   ├── courses/<course-id>.yml   # course metadata (title, description, FAQs, SEO)
│   ├── lessons/en/<course>/<lesson>.md
│   ├── slides/<course>/*.webp    # optional: imported lecture slides
│   ├── notes/<course>.yml        # optional: per-slide explanations
│   ├── RESOURCES.md              # optional library page
│   └── models/                   # optional model lab
│       ├── *.onnx                # exported, inspectable models
│       ├── graphs/*.json         # shapes + edges for the offline explorer
│       └── catalog.json
├── engine/                       # the content engine — knows no subject
│   ├── topics.py                 # loads topics, courses and lessons
│   ├── blocks.py                 # split rendered lesson HTML into blocks
│   └── tutorial.py               # the tutorial page presenter (steps + controls)
├── tools/
│   ├── build.py                  # static site baker: content + engine → site/
│   ├── import_lecture.py         # one command: PDF + captions → lessons + notes queue
│   ├── import_slides.py          # lecture PDF → slides + slide lessons
│   ├── align_transcript.py       # captions → which slide each sentence belongs to
│   └── export_models.py          # PyTorch → ONNX → graph JSON
├── assets/css/style.css
├── assets/js/{app,viz,graph}.js
└── site/                         # generated output (not source)
```

The content schema is deliberately plain: `courses/<id>.yml`, `lessons/<lang>/<course>/<lesson>.md`, YAML front matter, and `:::single-choice` checks. A lesson's path must agree with its `lesson_id`, `course_id` and `lang`.

## Topics

A topic is a complete curriculum: a folder under `content/` with its own `site.yml`, courses and lessons, plus optional extras. `topics.yml` lists which topics are published, and every topic is built into its own subtree:

```text
site/index.html                     topic chooser
site/<topic>/index.html             that curriculum's front page
site/<topic>/path.html              its guided path
site/<topic>/courses/…              its courses
site/<topic>/lessons/…              its lessons
site/search-index.json              one index across all topics
```

Adding a subject such as machine learning or deep learning takes no engine changes:

1. Create `content/ml/site.yml` with `title`, `tagline`, `description`, `levels`, `nav` and optional `hero`/`principles`/`features` blocks.
2. Add `content/ml/courses/<course-id>.yml` and `content/ml/lessons/en/<course>/<lesson>.md`.
3. Add `ml` to the `topics:` list in `topics.yml` and run the build.

The topic gets a card on the front page, its own navigation, progress tracking, search results and reader. The model lab and the resources page appear only when the topic has a `models/catalog.json` or a `RESOURCES.md`, so a text-only topic never links to a page it does not have.

## Importing a slide deck

A lecture deck can become a topic course without retyping anything. `tools/import_slides.py` reads the PDF, works out its structure and writes slide lessons plus WebP images:

```bash
python3 tools/import_slides.py --src /path/to/decks --lecture 1 --report   # inspect the parse
python3 tools/import_slides.py --src /path/to/decks --lecture 1            # write content
```

`tools/import_lecture.py` runs the whole chain for a lecture — find the PDF, import it, find the recording, download captions, align them, and open a notes entry per slide — leaving only the prose to write:

```bash
python3 tools/import_lecture.py --lecture 3 --src /path/to/decks
```

The lecture's sources are declared in the topic's `site.yml` (`source.pdf`, `source.playlist`), so the lecture number is the only argument needed once `--src` or `$SLIDES_DIR` points at the PDFs. The notes merge is append-only: `gist` text that already exists is never rewritten, so re-running after a better import or a new caption file cannot damage written explanations. Blank `gist` entries are the writing queue, and each new entry arrives with a verbatim quote already drafted from the transcript.

It handles what lecture decks actually do: Beamer overlay builds (several PDF pages animating one slide) are collapsed to the most complete page, the reprinted agenda pages become lesson boundaries — on the right or the left, as the deck draws them — and slide titles are read from the page layout rather than guessed from the first line of text. A deck with no agenda at all is cut into lesson-sized parts named after the slide each one opens on, and any section longer than twenty slides is split the same way, because a wall of eighty slides is not a lesson. Each remaining slide becomes one `:::slide` step, with its parsed text kept under the image and indexed for search.

Output is regenerated on every run, so hand edits to generated lessons are lost — change the importer instead. Stale lessons and leftover images from an earlier parse are cleared, and images that already exist are not re-rendered unless `--force` asks for it. The source PDFs stay out of the repository; only the rendered slides and their attribution do. Re-run with `--lecture 2`, `--lecture 3`, … to add the rest of a course, or pass several `--lecture` flags to do them all at once.

### Explaining the slides

A slide alone rarely teaches; `content/<topic>/notes/<course>.yml` holds one explanation per slide, keyed by PDF page number, and the build prints it under the image:

```yaml
29:
  gist: >-
    What the slide is saying, for a reader who was not in the room.
  said: >-
    An optional verbatim line from the lecturer.
```

The importer writes the lesson; the notes file is written by hand, one entry at a time, so a deck can be published first and explained gradually. Notes are also folded into the search index, which makes a slide searchable by what it *means* rather than by the words printed on it.

When the lecture recording is available, `tools/align_transcript.py` makes the writing accurate instead of guessed:

```bash
yt-dlp --skip-download --write-auto-subs --sub-langs en --sub-format vtt <video-url>
python3 tools/align_transcript.py --vtt <captions>.vtt --course lecture-01 --report
python3 tools/align_transcript.py --vtt <captions>.vtt --course lecture-01 --write
```

Captions carry no slide numbers and the deck carries no timestamps, so the two are matched as one monotonic partition of the transcript — every sentence belongs to exactly one slide, slides keep their order, and the total match is maximised. The draft it writes (`*.auto.yml`, git-ignored) is a working aid: the published notes are written from it in plain language, because a transcript narrates a lecture rather than summarising a slide.

## Engine and content

Content and presentation are separate. `content/` holds only writing — markdown, front matter and checks — and never mentions layout. `engine/` holds the reading machinery and knows nothing about the subject:

- `engine/topics.py` discovers topics from `topics.yml`, loads each topic's `site.yml`, courses and lessons, and exposes the topic's URL prefix. Missing topics are skipped rather than failing the build.
- `engine/blocks.py` splits rendered lesson HTML into top-level blocks (paragraph, heading, list, code, figure, callout, check).
- `engine/tutorial.py` is the tutorial page presenter. `present_tutorial(content, finish_href=…, finish_label=…)` groups the blocks into steps — one paragraph each, with its heading and any list, code, figure or check that belongs to it — and returns the step markup plus the controls. It decides nothing about the site: the caller supplies where the lesson ends.
- `tools/build.py` is the baker. It loads every topic, renders markdown, hands the HTML to the presenter, and writes one subtree per topic plus the chooser and the shared search index.

Adding a new presentation module (a quiz-only drill, a printable view) means adding a file under `engine/`; it never requires touching lesson text. Adding lessons or topics never requires touching the engine.

## Lesson directives

Beyond standard Markdown, five directives are supported:

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

:::slide{src="../../slides/lecture-01/slide-029.webp" n="29"} Slide title
- Text parsed from the slide.
:::

:::callout{type="warning" title="Short title"}
Markdown body.
:::
```

Available demo ids: `convolution`, `histogram`, `edges`, `pinhole`, `stereo`, `receptive`, `optimizer`, `diffusion`, `iou`.

Available model ids: `demo-cnn`, `resnet-mini`, `vit-tiny`, `unet-mini`, `mobilenet-block`.

## Features

- **One guided path per topic**: all of a curriculum's lessons in one numbered sequence with a progress bar and a continue button that jumps to the next unfinished lesson. Lesson pages link to the previous and next lesson *across course boundaries*, so you never have to go back to a menu to keep going.
- **Paragraph-by-paragraph lessons**: the engine presents one paragraph at a time (with whatever heading, list, code, figure or check belongs to it), a centred **Continue** button below it, and a progress meter. When a step ends in a check, Continue is disabled until the check is answered; a wrong option is eliminated so you can try again. The outline jumps to the step holding the heading, the footer pager appears only at the end, and without JavaScript the whole lesson renders as a single page.
- **Wide three-column lesson layout**: course navigation, a generously sized prose column, and an on-this-page outline that collapses below 1120px.
- **Progress tracking** in `localStorage`: completed lessons and solved checks persist per browser, keyed by topic so two curricula never share a checkbox.
- **Client-side search** across every topic over lesson text, courses and snippets, with keyboard navigation (`⌘K` or `/`).
- **Calculation blocks** rendered with KaTeX. Math falls back to readable plain text if the CDN is unavailable.
- **Light theme by default**, with a dark theme one click away in the header; the choice persists and is applied before first paint. Responsive down to mobile, reduced-motion support.
- **Generated course art** — deterministic SVG, no binary image assets or licensing questions.
- **Accessible fundamentals**: skip link, semantic landmarks, focusable quiz buttons, status announcements for feedback.

## Verification

```bash
python3 tools/build.py                     # prints counts per topic
python3 - <<'PY'
import json, pathlib
files = list(pathlib.Path("site").rglob("*.html"))
print(len(files), "pages")
json.load(open("site/search-index.json"))
json.load(open("site/vision/models/catalog.json"))
PY
```

The generator prints the lesson and course count for each topic and the output directory. Lessons whose front matter cannot be parsed are skipped rather than failing the whole build, so compare the printed lesson total against `ls content/vision/lessons/en/*/*.md` after structural edits.

## Content provenance and attribution

This curriculum was authored for this repository. The curated resource list draws on several public collections, credited in [content/vision/RESOURCES.md](content/vision/RESOURCES.md):

- [developer-roadmap](https://github.com/kamranahmedse/developer-roadmap) — ML, MLOps and AI red-teaming roadmaps used to cross-check topic coverage.
- [free-programming-books](https://github.com/EbookFoundation/free-programming-books) — free books and courses.
- [build-your-own-x](https://github.com/codecrafters-io/build-your-own-x) — from-scratch implementations.
- [awesome](https://github.com/sindresorhus/awesome) and the [awesome-computer-vision](https://github.com/jbhuang0604/awesome-computer-vision) list.
- [coding-interview-university](https://github.com/jwasham/coding-interview-university) — mathematical and algorithmic foundations.

Links point to their original authors and are not mirrored here.

## License

Content is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Code is MIT. Model files are generated by `tools/export_models.py` from standard architectural definitions and carry the same MIT licence.
