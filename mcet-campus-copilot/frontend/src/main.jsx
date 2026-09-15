import React, {useState} from "react"
import {createRoot} from "react-dom/client"
import {Bot, Sparkles, Target, Lightbulb, BookOpen, Briefcase, Upload, ArrowRight, Check} from "lucide-react"
import "./styles.css"

const API = import.meta.env.VITE_API_URL || "http://localhost:8000"

const agents = [
  ["auto","Auto Agent",Sparkles],
  ["goal","Goal Planner",Target],
  ["opportunity","Opportunities",Briefcase],
  ["project","Project Agent",Lightbulb],
  ["academic","Academic Agent",BookOpen],
]

function App(){
  const [goal,setGoal] = useState("")
  const [agent,setAgent] = useState("auto")
  const [context,setContext] = useState("")
  const [loading,setLoading] = useState(false)
  const [data,setData] = useState(null)
  const [file,setFile] = useState(null)

  async function run(){
    if(!goal.trim()) return
    setLoading(true); setData(null)
    try{
      const res = await fetch(`${API}/api/copilot`,{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({goal,agent,context})
      })
      setData(await res.json())
    }catch(e){
      setData({agent,trace:["Understand","Analyze","Plan","Generate"],title:"Connection error",result:"Start the FastAPI backend first, then try again."})
    }finally{setLoading(false)}
  }

  async function upload(){
    if(!file) return
    setLoading(true)
    const form = new FormData()
    form.append("file",file); form.append("goal",goal)
    try{
      const res = await fetch(`${API}/api/copilot/upload`,{method:"POST",body:form})
      setData(await res.json())
    }catch(e){
      setData({agent:"academic",trace:["Understand","Analyze","Plan","Generate"],title:"Upload error",result:"Could not connect to the backend."})
    }finally{setLoading(false)}
  }

  return <div className="app">
    <header>
      <div className="brand"><div className="logo"><Bot size={22}/></div><div><b>MCET Campus Copilot</b><span>AI Agent for Student Success</span></div></div>
      <div className="pill">● LOCAL MVP</div>
    </header>

    <main>
      <section className="hero">
        <div className="eyebrow"><Sparkles size={15}/> YOUR CAMPUS, ONE COPILOT</div>
        <h1>Turn a goal into<br/><em>your next move.</em></h1>
        <p>Tell the Copilot what you want to achieve. It understands your goal, chooses the right workflow, and creates an actionable plan.</p>
      </section>

      <section className="workspace">
        <div className="panel input-panel">
          <label>What do you want to achieve?</label>
          <textarea value={goal} onChange={e=>setGoal(e.target.value)} placeholder="e.g. I want to build an AI project for my final year and prepare it for a hackathon..." />
          <label>Choose workflow</label>
          <div className="agent-grid">{agents.map(([id,name,Icon])=>
            <button className={agent===id?"agent active":"agent"} onClick={()=>setAgent(id)} key={id}><Icon size={17}/><span>{name}</span></button>
          )}</div>
          <label>Extra context <small>(optional)</small></label>
          <textarea className="small" value={context} onChange={e=>setContext(e.target.value)} placeholder="Paste notes, requirements, or other context..." />
          <div className="upload">
            <Upload size={18}/>
            <input type="file" accept=".txt,.md,.csv,.json" onChange={e=>setFile(e.target.files?.[0]||null)}/>
            {file && <button onClick={upload}>Analyze file</button>}
          </div>
          <button className="run" onClick={run} disabled={loading || !goal.trim()}>
            {loading ? "Copilot is thinking..." : <>Run Copilot <ArrowRight size={18}/></>}
          </button>
        </div>

        <div className="panel result-panel">
          {!data ? <div className="empty"><div className="empty-icon"><Bot size={30}/></div><h2>Your AI workspace</h2><p>Your agent trace and actionable result will appear here.</p></div> :
          <><div className="trace"><div className="trace-title">AGENT TRACE</div><div className="trace-row">{data.trace?.map((x,i)=><React.Fragment key={x}><div className="trace-step"><div className="check"><Check size={13}/></div><span>{x}</span></div>{i<data.trace.length-1 && <div className="line"/>}</React.Fragment>)}</div></div>
          <div className="answer"><div className="answer-meta"><span>{data.agent?.toUpperCase()} AGENT</span></div><h2>{data.title}</h2><div className="result">{data.result}</div></div></>}
        </div>
      </section>
    </main>
    <footer>MCET Campus Copilot · Functional AI Agent MVP</footer>
  </div>
}
createRoot(document.getElementById("root")).render(<App/>)
