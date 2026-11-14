# Contributing to Madarik

Madarik (مدارِك) is a content-first learning platform: independent curricula built by a small, dependency-free static engine. Vision Journey is its first curriculum. Contributions are welcome for lessons, corrections, interactive labs, models, resource lists and new topics.

## Ground rules

- Keep a pull request focused on one topic, and change no more than a few files unless the change is a curriculum restructure.
- Write new lessons in English under `content/<topic>/lessons/en/`.
- Preserve accuracy above all: every factual claim should be checkable against a primary source or a standard text.
- Run the build and the checks below before opening the PR.
- Do not add a lesson that duplicates an existing one. Extend or split rather than repeat.

## Repository structure

```text
topics.yml                                    the topics that get published
content/<topic>/site.yml                      topic metadata, levels, nav, hero copy
content/<topic>/courses/<course-id>.yml       course metadata
content/<topic>/lessons/<lang>/<course-id>/<lesson>.md
content/<topic>/RESOURCES.md                  optional library page
content/<topic>/models/                       optional ONNX + graph JSON + catalog
engine/topics.py                              loads topics, courses and lessons
engine/tutorial.py                            tutorial page presenter (steps, Continue)
engine/blocks.py                              splits rendered lessons into blocks
tools/build.py                                static site baker
tools/export_models.py                        PyTorch → ONNX → graph JSON
assets/{css,js}/                              presentation and interaction
```

A new subject is a new folder under `content/` plus one line in `topics.yml`; the `vision` topic is simply the first one.

## Adding a topic

Topics are content, not code. To add machine learning, deep learning or anything else:

1. Create `content/<id>/site.yml` with `title`, `tagline`, `description`, `levels` and `nav`. Optional blocks:
   - `hero` — `eyebrow`, `title`, `lede`, `rail_title` for the front page (Markdown emphasis allowed in `title` and `lede`);
   - `principles` — a list of `{title, text}` cards;
   - `timeline` — `{year, event}` entries for the front-page rail;
   - `features.labs` — the number of interactive labs to advertise.
2. Add courses under `content/<id>/courses/` and lessons under `content/<id>/lessons/en/<course>/`.
3. Add the id to `topics:` in `topics.yml` and run `python3 tools/build.py`.

The topic gets its own subtree in `site/`, a card on the front page, its own guided path, progress tracking, search entries and reader. Leave out `models/` and `RESOURCES.md` and the model lab and library pages are simply not built or linked. If the topic needs the model lab, copy the export script output into `content/<id>/models/` and point `tools/export_models.py` at that folder.

Do not add subject-specific branches to `tools/build.py` or `engine/`. If a new topic needs a genuinely new kind of page, add a module under `engine/` that takes content in and returns markup — the same way `engine/tutorial.py` does.

IDs and directory names use lowercase kebab-case. A lesson's path must agree with its `lesson_id`, `course_id` and `lang`: `content/vision/lessons/en/recognition/object-detection.md` belongs to the `vision` topic's `recognition` course, has lesson ID `object-detection`, and declares `lang: "en"`.

## Course metadata

Each course is defined in `content/<topic>/courses/<course-id>.yml`:

```yaml
id: recognition
category:
  id: deep-vision
order_index: 7
translations:
  en:
    title: "Recognition: Classification, Detection, Segmentation"
    description: "A concise description of the course's scope."
    faqs:
      - question: "A question a learner would actually ask?"
        answer: "A clear, self-contained answer."
    meta_title: "Recognition - Vision Journey"
    meta_description: "A specific, search-friendly description."
    meta_keywords: "comma, separated, keywords"
```

The filename and `id` must match. `category.id` must be one of the levels in the topic's `site.yml`, and `order_index` must be unique across that topic because it determines the course order there.

The three FAQs are rendered on the course page and used for search snippets. Write them as real learner questions, not as marketing copy.

## Lesson format

Front matter, in this order:

```yaml
---
lesson_id: "object-detection"
course_id: "recognition"
lang: "en"
order_index: 2
title: "Object Detection"
description: "One sentence describing what the lesson establishes."
meta_title: "Object Detection - Recognition"
meta_description: "A specific description for search engines."
meta_keywords: "object detection, IoU, mAP"
---
```

- `order_index` is an unquoted integer, unique within the course and language.
- `description` is one sentence. It appears on course pages and in search results.
- `meta_title` normally follows `Lesson Title - Course Title`.

### Body structure

- Do **not** add a level-one heading; the site renders `title` as the page heading.
- Use `##` for top-level sections and lower levels only for genuine hierarchy.
- Open with a paragraph that states the problem the lesson solves.
- Explain an idea before asking a question about it.
- End with `## Summary`: one short sentence, then no more than five numbered outcomes.
- Prefer concrete numbers, derivations and failure modes over adjectives.

### Checks

Every lesson should contain three to five meaningful single-choice checks, placed immediately after the material they assess:

```markdown
:::single-choice{#unique-component-id} Why does a homography need four correspondences?

::option[Because each correspondence supplies two equations, and it has eight degrees of freedom]{#h-dof .correct explanation="Eight equations determine the eight independent entries."}
::option[Because two points define a line]{#h-line explanation="Lines are not what a homography parameterises."}
::option[Because SVD requires a square matrix]{#h-svd explanation="The design matrix is rectangular; SVD handles that fine."}
:::
```

Rules:

- the question goes on the same line as `:::single-choice{...}`;
- exactly three plausible options and exactly one `.correct`;
- every option has a specific, non-empty `explanation`;
- lowercase kebab-case IDs, unique across the English curriculum;
- the question must be answerable from content that appears before it;
- vary which position holds the correct answer.

Two parser constraints matter:

1. **Avoid `]` inside option labels**, including inline code. The parser treats the first `]` as the end of the label. Character classes are fine in question text and explanations.
2. **Avoid `}` inside explanations**, including quoted ones. The parser treats the first `}` as the end of the attributes. Describe a brace placeholder in words.

### Labs and model embeds

Interactive labs are mounted by ID. The body is rendered as Markdown below the canvas:

```markdown
:::demo{id="edges"} Threshold, operator and edge density
Lower the threshold and watch noise enter as spurious edges.
:::
```

Available IDs are defined in `assets/js/viz.js`: `convolution`, `histogram`, `edges`, `pinhole`, `stereo`, `receptive`, `optimizer`, `diffusion`, `iou`. Adding a lab means adding a function to the `DEMOS` registry; it receives the stage element and must build its own controls.

Model graphs are embedded by ID from the topic's `models/graphs/`:

```markdown
:::model{src="resnet-mini"} ResNet-Mini: identity shortcuts as graph edges
:::
```

### Callouts

```markdown
:::callout{type="warning" title="Check the DC response"}
The body is Markdown.
:::
```

Types: `note` (default), `insight`, `warning`, `danger`.

### Math

Inline math uses single dollars: `$x = fX/Z$`. Display math uses double dollars on their own lines and may span multiple lines. Both render with KaTeX and fall back to readable text without it. Do not use `$` for currency in a lesson.

## Adding or changing a model

`tools/export_models.py` defines each architecture as a small `nn.Module`, exports it with `torch.onnx.export`, runs shape inference, and writes:

- `content/<topic>/models/<id>.onnx` — the real model file, inspectable in Netron;
- `content/<topic>/models/graphs/<id>.json` — nodes, edges, shapes and parameter counts;
- `content/<topic>/models/catalog.json` — the metadata shown on the Model Lab page.

To change a model, edit the module and the `MODELS_SPEC` entry (including its stage rules for graph collapsing), then:

```bash
python3 tools/export_models.py
python3 tools/build.py
```

Guidelines:

- keep models small (well under a few megabytes) so the repository stays light;
- use fixed input shapes for a deterministic graph;
- call `model.eval()` and export with a fixed opset;
- verify the graph renders and that shapes match the architecture you describe;
- do not commit a model whose weights encode a licensed dataset.

## Building and verifying

```bash
python3 tools/build.py
python3 -m http.server -d site 8000
```

Open `http://localhost:8000` and check:

- the lesson renders, with no literal `:::` or `$` left in the page;
- every check accepts one answer and shows explanations;
- the lab controls respond;
- the embedded graph renders and a node click shows shapes;
- previous/next links and the sidebar point to existing pages.

A useful content check:

```bash
# every lesson has exactly three checks and a Summary
for f in content/*/lessons/en/*/*.md; do
  n=$(grep -c '^:::single-choice' "$f")
  s=$(grep -c '^## Summary' "$f")
  printf '%-70s checks=%s summary=%s\n' "$f" "$n" "$s"
done
```

Optional SEO check, when `trafilatura` is installed:

```bash
python3 -m trafilatura.cli --validate-seo site
```

## Writing guidelines

- Define technical terms on first use, and state units.
- Prefer a concrete example with numbers over an abstract description.
- Distinguish what is proved, what is empirically observed, and what is contested.
- Attribute claims to papers, standards or named implementations.
- Give the failure mode: what breaks, and how you would notice.
- Do not present a single benchmark number as a general claim about a capability.
- Avoid hype. "State of the art" needs a date, a dataset and a metric.

## Translation

This repository currently ships English content only. A translation directory may be added under `content/<topic>/lessons/<lang>/`; it must mirror the course structure and preserve all IDs, code, links, paths and directive syntax. Do not add machine-generated translations without native review.

## Commit messages

Use direct, scoped messages:

```text
Add lesson: Diffusion models
Fix stereo depth derivation
Replace dead SIFT link
Export MobileNet block model
```

## Reporting problems

Open an issue if a correction needs discussion or a course placement is unclear. For factual errors, include the claim, the source that contradicts it, and a suggested correction. Keep discussion learner-focused.

Thank you for helping make rigorous computer vision education freely available.
