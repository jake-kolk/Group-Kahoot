import { useEffect, useRef, useState } from 'react'
import './App.css'

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
