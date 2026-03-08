# Agent

AI Desktop Assistant with LangGraph and Ollama

## Structure

```
agent/
├── backend/           # Python AI backend
│   ├── src/agent/     # Main package
│   ├── pyproject.toml
│   └── Pipfile
└── desktop/           # Electron desktop UI
    ├── main.js
    └── index.html
```

## Setup

**Backend:**
```bash
cd backend
pip install pipenv
pipenv install
pipenv run python -m agent.cli
```

**Desktop:**
```bash
cd desktop
npm install
npm start
```
