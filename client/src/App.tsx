import { useEffect, useRef, useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function AppOld() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

function App() {
  
  const wsRef = useRef<WebSocket>(null); //useRef so that it doesn't get reloaded on rerender
  const [name, setName] = useState<string>('');
  const [log, setLog] = useState<string[]>([]);

  useEffect(() => {
    wsRef.current = new WebSocket("ws://localhost:8080/ws");
    wsRef.current.onopen = () => addToLog("Connected to Websocket");
    wsRef.current.onmessage = event => {
      addToLog(event.data);
    }
    wsRef.current.onclose = () => console.log("Websocket closed");

    return () => wsRef.current?.close();
  }, []);

  const addToLog = (msg: string) => {
    setLog(prev => [...prev, msg]);
  }

  const handleJoin = () => {
    if (!name) return;
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({type: 'join', room: 'ABCD', name}));
    }
  }

  return (
    <>
      <h3>Kahoot clone - demo client</h3>
      <input id='name' placeholder='Name' value={name} onChange={e => setName(e.target.value)}></input><button id='join' onClick={handleJoin}>Join</button>
      <div id='log' style={{ marginTop: '1rem' }}>
        {log.map((msg, i) => (
          <div key={i}>{msg}</div>
        ))}
      </div>
    </>
  )
}

export default App
