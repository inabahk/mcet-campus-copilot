import os
from google import genai
from models import CopilotResponse

SYSTEM = """
You are MCET Campus Copilot, a practical AI agent for college students.
Your job is to understand a student's goal, choose or follow the requested workflow,
and return useful, realistic, actionable output.

Available workflows:
- goal: convert a goal into a step-by-step action plan
- opportunity: identify and organize relevant opportunity types from supplied context
- project: generate project ideas, roles, stack and roadmap
- academic: turn study material/context into a study plan and quiz
- auto: choose the best workflow yourself

Always be concise, structured and student-friendly. Do not invent specific college
deadlines, events, links, or opportunities unless they are supplied in the context.
"""

def choose_agent(goal, requested):
    if requested and requested != "auto":
        return requested
    g = goal.lower()
    if any(x in g for x in ["project", "build", "app", "idea"]):
        return "project"
    if any(x in g for x in ["exam", "study", "subject", "quiz", "notes"]):
        return "academic"
    if any(x in g for x in ["internship", "hackathon", "opportunity", "competition"]):
        return "opportunity"
    return "goal"

def fallback(agent, goal, context):
    templates = {
        "goal": f"Goal: {goal}\\n\\n1. Define the target outcome.\\n2. Break it into weekly tasks.\\n3. Gather required resources.\\n4. Complete the highest-priority task first.\\n5. Review progress and adjust.",
        "project": f"Project: {goal}\\n\\n• Core idea\\n• Suggested stack: React, FastAPI, Python\\n• Roles: AI/Backend, Frontend, Data/Research\\n• Roadmap: Problem → MVP → Testing → Deployment → Demo",
        "academic": f"Study goal: {goal}\\n\\n• Identify topics\\n• Prioritize difficult topics\\n• Study in short focused blocks\\n• Practice questions\\n• Take a self-quiz\\n\\nQuiz starter:\\n1. What is the main concept?\\n2. Explain it in your own words.\\n3. Give one example.",
        "opportunity": f"Opportunity goal: {goal}\\n\\n• Define eligibility\\n• Prepare CV/GitHub/portfolio\\n• Shortlist relevant opportunities\\n• Track deadlines\\n• Apply and record status."
    }
    return templates.get(agent, templates["goal"])

async def run_agent(goal, requested="auto", context=""):
    agent = choose_agent(goal, requested)
    trace = ["Understand", "Analyze", "Plan", "Generate"]

    key = os.getenv("GEMINI_API_KEY")
    if not key:
        return CopilotResponse(
            agent=agent,
            trace=trace,
            title="Local Demo Result",
            result=fallback(agent, goal, context)
        )

    try:
        client = genai.Client(api_key=key)
        prompt = f"""{SYSTEM}

Workflow: {agent}
Student goal: {goal}
Additional context:
{context[:20000]}

Return:
1. A short title
2. A practical answer with headings and bullets
3. For project workflow include idea, roles, tech stack and roadmap
4. For academic workflow include study plan and 5-question quiz
5. For opportunity workflow include a useful tracking/action structure
"""
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )
        text = response.text or fallback(agent, goal, context)
        title = text.splitlines()[0].replace("#", "").strip()[:100] or "Campus Copilot Result"
        return CopilotResponse(agent=agent, trace=trace, title=title, result=text)
    except Exception:
        return CopilotResponse(
            agent=agent,
            trace=trace,
            title="Campus Copilot Result",
            result=fallback(agent, goal, context)
        )
