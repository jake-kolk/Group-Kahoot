import { useEffect, useRef, useState } from 'react'
import './App.css'

function App() {
  const wsRef = useRef<WebSocket | null>(null)
  const timerRef = useRef<NodeJS.Timeout | null>(null)

  const [name, setName] = useState('')
  const [roomCode, setRoomCode] = useState('')
  const [log, setLog] = useState<string[]>([])
  const [joined, setJoined] = useState(false)
  const [gameStarted, setGameStarted] = useState(false)
  const [question, setQuestion] = useState('')
  const [answers, setAnswers] = useState<string[]>([])
  const [questionId, setQuestionId] = useState<number | null>(null)
  const [selectedOption, setSelectedOption] = useState<number | null>(null)
  const [duration, setDuration] = useState<number | null>(null)
  const [timeLeftMs, setTimeLeftMs] = useState<number>(0)
  const [questionEnded, setQuestionEnded] = useState(false)

  // WebSocket setup
  useEffect(() => {
    connectWebSocket()
    return () => wsRef.current?.close()
  }, [])

  const connectWebSocket = () => {
    wsRef.current = new WebSocket(`ws://${window.location.host}/ws/`)
    wsRef.current.onopen = () => addToLog('Connected to WebSocket')

    wsRef.current.onmessage = (event) => {
      const data = JSON.parse(event.data)
      addToLog(`Received: ${event.data}`)

      if (data.type === 'player_leave') {
        // handler for player leave
      }

      if (data.type === 'question') {
        setQuestion(data.text)
        setAnswers(data.choices)
        setQuestionId(data.question_id)
        setDuration(data.duration_ms)
        setSelectedOption(null)
        setQuestionEnded(false)
        setGameStarted(true)

        // start timer
        setTimeLeftMs(data.duration_ms)
        if (timerRef.current) clearInterval(timerRef.current)
        timerRef.current = setInterval(() => {
          setTimeLeftMs((prev) => {
            if (prev <= 1000) {
              clearInterval(timerRef.current!)
              handleQuestionTimeout()
              return 0
            }
            return prev - 1000
          })
        }, 1000)
      }

      if (data.type === 'question_ended') {
        clearInterval(timerRef.current!)
        setQuestionEnded(true)
      }

      if (data.type === 'leaderboard') {
        addToLog('Leaderboard:')
        data.top.forEach((p: any) => addToLog(`${p.name}: ${p.points} pts`))
      }
    }

    if (wsRef.current?.readyState != WebSocket.OPEN) {
      addToLog('WebSocket is not open — connection may be closed.')
    }
  }

  const addToLog = (msg: string) => setLog((prev) => [...prev, msg])

  const handleJoin = () => {
    if (!name || !roomCode) {
      addToLog('Please enter both name and room code.')
      return
    }
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ type: 'join', room: roomCode, name }))
      setJoined(true)
      addToLog(`Joined room ${roomCode} as ${name}`)
    } else {
      addToLog('WebSocket connection not ready.')
    }
  }

  const handleDisconnect = () => {
    if (wsRef.current) {
      wsRef.current.send(JSON.stringify({ type: 'player_leave', room: roomCode, name }))
      clearInterval(timerRef.current!)
      setJoined(false)
      setGameStarted(false)
      setQuestion('')
      setAnswers([])
      setQuestionEnded(false)
      setSelectedOption(null)
      setLog((prev) => [...prev, 'Left Game'])
    }
  }

  const handleStartGame = () => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ type: 'start_game', room: roomCode, name }))
      addToLog(`Game started by ${name}`)
    }
  }

  const handleOptionChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSelectedOption(parseInt(e.target.value))
  }

  const handleSendAnswer = () => {
    if (
      wsRef.current?.readyState === WebSocket.OPEN &&
      selectedOption !== null &&
      questionId !== null
    ) {
      wsRef.current.send(
        JSON.stringify({
          type: 'answer',
          question_id: questionId,
          choice: selectedOption,
          time_left_ms: timeLeftMs,
        })
      )
      addToLog(`Sent answer: ${selectedOption} (${answers[selectedOption]})`)
      clearInterval(timerRef.current!)
      setQuestionEnded(true)
    }
  }

  const handleQuestionTimeout = () => {
    addToLog('Time is up!')
    setQuestionEnded(true)
  }

  return (
    <div style={{ padding: '1rem', position: 'relative' }}>
      <h3>Kahoot Clone - Demo Client</h3>

      {/* ✅ Persistent Disconnect Button */}
      {joined && (
        <button
          onClick={handleDisconnect}
          style={{
            position: 'absolute',
            top: '1rem',
            right: '1rem',
            backgroundColor: '#e63946',
            color: 'white',
            border: 'none',
            padding: '0.5rem 1rem',
            borderRadius: '8px',
            cursor: 'pointer',
          }}
        >
          Leave Game
        </button>
      )}

      {/* --- JOIN SCREEN --- */}
      {!joined && (
        <>
          <input
            id="name"
            placeholder="Enter your name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            style={{ display: 'block', marginBottom: '0.5rem' }}
          />
          {/* ✅ New Room Code Field */}
          <input
            id="room"
            placeholder="Enter room code"
            value={roomCode}
            onChange={(e) => setRoomCode(e.target.value)}
            style={{ display: 'block', marginBottom: '0.5rem' }}
          />
          <button id="join" onClick={handleJoin}>
            Join
          </button>
        </>
      )}

      {/* --- LOBBY SCREEN --- */}
      {joined && !gameStarted && (
        <div style={{ marginTop: '1rem' }}>
          <p>Welcome, {name}! (Room: {roomCode})</p>
          <button onClick={handleStartGame}>Start Game</button>
        </div>
      )}

      {/* --- QUESTION SCREEN --- */}
      {joined && gameStarted && !questionEnded && (
        <div style={{ marginTop: '1rem' }}>
          <h4>{question || 'Waiting for next question...'}</h4>
          {duration && (
            <p>⏳ Time left: {Math.ceil(timeLeftMs / 1000)} seconds</p>
          )}

          <div onChange={handleOptionChange}>
            {answers.map((choice, i) => (
              <label key={i} style={{ display: 'block', marginBottom: '0.5rem' }}>
                <input
                  type="radio"
                  name="choice"
                  value={i}
                  checked={selectedOption === i}
                  onChange={handleOptionChange}
                />
                {` ${choice}`}
              </label>
            ))}
          </div>

          <button
            disabled={selectedOption === null || timeLeftMs <= 0}
            onClick={handleSendAnswer}
          >
            Send Answer
          </button>
        </div>
      )}

      {/* --- QUESTION ENDED SCREEN --- */}
      {joined && gameStarted && questionEnded && (
        <div style={{ marginTop: '1rem' }}>
          <h4>✅ Question Ended!</h4>
          <p>Waiting for the next question...</p>
          <p>(Leaderboard and next question will appear automatically)</p>
        </div>
      )}

      {/* --- LOG AREA --- */}
      <div id="log" style={{ marginTop: '1rem' }}>
        {log.map((msg, i) => (
          <div key={i}>{msg}</div>
        ))}
      </div>
    </div>
  )
}

export default App
