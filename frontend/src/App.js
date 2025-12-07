import React, { useState, useEffect, useRef } from "react";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [listening, setListening] = useState(false);

  const chatEndRef = useRef(null);
  const recognitionRef = useRef(null);

  // Auto-scroll
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Send message
  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);

    const response = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: input }),
    });

    const data = await response.json();
    const botMessage = { role: "bot", text: data.reply };
    setMessages((prev) => [...prev, botMessage]);

    setInput("");
  };

  // Start listening (continuous mode)
  const startListening = () => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert("Speech recognition not supported.");
      return;
    }

    if (!recognitionRef.current) {
      const recognition = new SpeechRecognition();
      recognition.lang = "en-US";
      recognition.continuous = true;
      recognition.interimResults = true;
      recognitionRef.current = recognition;
    }

    const recognition = recognitionRef.current;

    let finalTranscript = "";
    setListening(true);
    recognition.start();

    recognition.onresult = (event) => {
      let interim = "";

      for (let i = 0; i < event.results.length; i++) {
        const text = event.results[i][0].transcript;
        if (event.results[i].isFinal) finalTranscript += text + " ";
        else interim += text;
      }
      setInput(finalTranscript + interim);
    };

    recognition.onerror = () => setListening(false);

    recognition.onend = () => {
      // Do NOT auto-restart if user intentionally stopped listening
      if (listening) recognition.start();
    };
  };

  // Stop listening
  const stopListening = () => {
    setListening(false);
    recognitionRef.current?.stop();
  };

  return (
    <div className="app-container">
      <header className="chat-header">Credit Card Assistant</header>

      <div className="chat-window">
        {messages.map((msg, i) => (
          <div key={i} className={`chat-message ${msg.role}`}>
            {msg.text}
          </div>
        ))}
        <div ref={chatEndRef}></div>
      </div>

      <div className="input-section">

        {/* 🎤 MIC BUTTON */}
        <button
          className={`mic-btn ${listening ? "recording" : ""}`}
          onClick={listening ? stopListening : startListening}
        >
          🎤
        </button>

        {/* TEXT INPUT */}
        <input
          className="chat-input"
          value={input}
          placeholder={listening ? "Listening..." : "Type a message..."}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              e.preventDefault();

              // Always stop recording before sending
              if (listening) {
                stopListening();
              }

              // Delay ensures speech recognition fully stops
              setTimeout(() => {
                sendMessage();
              }, 80);
            }
          }}
        />

        {/* SEND BUTTON */}
        <button className="send-btn" onClick={sendMessage}>
          ➤
        </button>
      </div>
    </div>
  );
}

export default App;
