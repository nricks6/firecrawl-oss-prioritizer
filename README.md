# OSS‑Issue‑Prioritizer ⚡️

CLI tool that fetches open issues from any GitHub repository, runs them through an LLM, and labels each one **P0 / P1 / P2** for instant triage.

Built with **Python**, **OpenAI**, **PyGitHub**, **Rich**, and AI‑assisted coding in **Cursor**.

---

## ✨ Features

- 🔖 **Priority tagging** – deterministic GPT‑4o call per batch of 10 issues  
- 🟥🟨🟩 **Color‑coded output** – terminal table via Rich for quick scanning  
- 🛠 **Single‑file script** (< 120 LOC) – easy to read, fork, or embed in CI  
- 🔐 **.env support** – keep API keys out of source control  
- ⚙️ **Configurable** – point at any repo and set a custom issue cap (`--top`)

---

1. Clone & Install

git clone https://github.com/nricks6/firecrawl-oss-prioritizer.git
cd oss-prioritizer
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

---

2. Add Secrets

Add secrets to .env file in project root:

GITHUB_TOKEN=ghp_yourPersonalAccessToken
OPENAI_API_KEY=sk-yourOpenAIKey

---

3. Run

# default: Firecrawl repo, top 50 issues
python classify.py

# any repo + custom cap
python classify.py openai/openai-python --top 20

---

Project Structure

.
├─ classify.py       # main script
├─ requirements.txt  # runtime dependencies
├─ .env.example      # sample env file
└─ README.md

---

Limitations & TODOs

1. No caching yet – large repos make multiple OpenAI calls.
2. Minimal error‑handling; quota or network errors surface directly.
