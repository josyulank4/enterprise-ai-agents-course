# Course Code — Udemy & Skool Programs

Official code companion for Naveen Kumar Josyula's courses (AIsoltrics
Technologies). This one repo serves both the Udemy and Skool programs:
every demo from every course runs here — no stubs, no slides-only code.
Clone it, run it, adapt it to your own enterprise.

## Course 1 — Enterprise AI Agents: From Pilot to Production (Udemy)

### What's inside (Course 1)

| Folder | Course lesson | What it is |
|--------|---------------|------------|
| `demo-rag-pipeline/` | Lesson 16 — [DEMO] Build a RAG Pipeline Walkthrough | Working RAG over sample enterprise docs: ingestion, chunking, TF-IDF retrieval, permission filtering, freshness checks, groundedness eval |
| `demo-tool-contract/` | Lesson 21 — [DEMO] Design a Tool Contract | Enterprise ticket API wrapped as agent tools: function schemas, validation, auth scoping, write-confirmation, rate limits, audit log, MCP manifest |
| `demo-eval-suite/` | Lessons 29–30 — [DEMO] Run an Eval Suite / Evals in CI/CD | Golden dataset, 4 scorers, latency + cost metrics, and a CI quality gate that blocks bad deployments |
| `capstone-template/` | Lessons 48–49 — Capstone Brief / Walkthrough | 10-part production design document template with a fully worked invoice-agent example and grading rubric |

## Prerequisites

- Python 3.9+
- No API keys required — every demo runs fully offline. (The eval suite has
  an *optional* LLM-as-judge path if you set `OPENAI_API_KEY`; the default
  heuristic judge needs nothing.)

## Quickstart

```bash
git clone https://github.com/josyulank4/enterprise-ai-agents-course.git
cd enterprise-ai-agents-course

# 1. RAG pipeline (Lesson 16)
cd demo-rag-pipeline && pip install -r requirements.txt && python rag_pipeline.py && cd ..

# 2. Tool contract (Lesson 21)
cd demo-tool-contract && python demo.py && cd ..

# 3. Eval suite + CI gate (Lessons 29-30)
cd demo-eval-suite && python eval_runner.py && python ci_gate.py && cd ..
```

Each folder has its own `README.md` with full run instructions, configuration
options, expected output, and guidance on adapting the demo to your own
systems.

## Course 2 — RAG Architecture: Production-Grade Retrieval Systems (Udemy)

**Folder:** `course-2-rag-architecture/`

The full production RAG pipeline from the course: ingestion, chunking,
embeddings, hybrid search (BM25 + dense + RRF), reranking, and a golden-set
evaluation harness with a release quality gate. Runs fully offline
(Python stdlib + numpy, no API keys); the embedding lesson uses a
deterministic local hashing vectorizer so results are identical on every run.

```bash
cd course-2-rag-architecture
pip install -r requirements.txt
python validate.py   # runs every demo end-to-end; must exit 0
```

Each demo also runs standalone — see the folder's `README.md` for the
lesson-by-lesson command map (L13 ingestion, L16–L17 chunking lab, L19–L22
embeddings lab, L28–L29 hybrid search, L30 reranking demo, L39 evaluation
harness demo).

## Course mapping (Course 1)

- **Build the case (S1)** → use the ROI framing in `capstone-template/` part 1
- **Build the system (S2–S6)** → `demo-rag-pipeline/`, `demo-tool-contract/`
- **Run it in production (S7–S11)** → `demo-eval-suite/`, `capstone-template/` parts 7–10
- **Capstone (S13)** → `capstone-template/capstone-design-template.md`

## Contributing / issues

This repo accompanies the course. Questions? Ask in the course Q&A on Udemy.

## License

MIT — use it in your own enterprise work.
