# MCET Campus Copilot

A functional AI-agent MVP for college students.

## Features
- Goal Planner Agent
- Opportunity Agent
- Project Agent
- Academic Agent
- Agent Trace: Understand → Analyze → Plan → Generate
- Text/context and document upload
- Gemini API integration
- React/Vite frontend
- FastAPI backend

## Run locally

### 1. Backend
```bash
cd backend
python -m venv venv
```

Windows:
```bash
venv\Scripts\activate
```

Mac/Linux:
```bash
source venv/bin/activate
```

Install:
```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your Gemini API key.

Start:
```bash
uvicorn main:app --reload
```

Backend runs at `http://localhost:8000`.

### 2. Frontend

Open a second terminal:
```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal, usually `http://localhost:5173`.

## Optional frontend API URL

Create `frontend/.env`:
```env
VITE_API_URL=http://localhost:8000
```

## Deployment

The backend contains `render.yaml` for Render deployment. After deploying the backend, set `VITE_API_URL` in the frontend deployment to the backend URL.

## Important

Never commit `.env` or API keys to GitHub.
