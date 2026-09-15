import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from models import CopilotRequest, CopilotResponse
from agent import run_agent

load_dotenv()

app = FastAPI(title="MCET Campus Copilot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok", "message": "MCET Campus Copilot API is running"}

@app.post("/api/copilot", response_model=CopilotResponse)
async def copilot(request: CopilotRequest):
    return await run_agent(request.goal, request.agent, request.context)

@app.post("/api/copilot/upload")
async def upload_document(file: UploadFile = File(...), goal: str = Form("")):
    content = await file.read()
    text = content.decode("utf-8", errors="ignore")[:20000]
    result = await run_agent(goal or "Create a study plan from this material", "academic", text)
    return result
