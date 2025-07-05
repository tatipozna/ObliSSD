import { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import { chatService } from "../services/api";
import "./Chat.css";

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    const userMessage = inputValue.trim();
    const currentTime = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

    setMessages((prev) => [...prev, { text: userMessage, sender: "user", time: currentTime }]);
    setInputValue("");
    setIsLoading(true);

    try {
      const response = await chatService.sendMessage(userMessage);
      const botTime = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

      setMessages((prev) => [...prev, { text: response.respuesta, sender: "bot", time: botTime }]);
    } catch (error) {
      console.error("Error al conectar con el servidor:", error);
      const errorTime = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

      setMessages((prev) => [
        ...prev,
        { text: error.message || "Error al conectar con el servidor", sender: "bot", time: errorTime },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h2>Tienda Alemana</h2>
        <p>Asistente virtual para consultas sobre productos y locales</p>
      </div>

      <div className="messages-container">
        {messages.length === 0 && (
          <div className="welcome-message">
            <h3>¡Willkommen!</h3>
            <p>Bienvenido a Tienda Alemana. Puedo ayudarte con información sobre:</p>
            <ul>
              <li>🛍️ Catálogo de productos alemanes</li>
              <li>📍 Información de nuestros locales</li>
              <li>🗺️ Ubicación física de productos</li>
            </ul>
            <p>¿En qué puedo ayudarte hoy?</p>
          </div>
        )}

        {messages.map((message, index) => (
          <div key={index} className={`message ${message.sender}`}>
            {message.sender === "bot" ? (
              <div className="message-bot message-content">
                <ReactMarkdown>{message.text}</ReactMarkdown>
              </div>
            ) : (
              <div className="message-user message-content">{message.text}</div>
            )}
            <div className="message-time">{message.time}</div>
          </div>
        ))}

        {isLoading && (
          <div className="message bot">
            <div className="message-content loading">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="input-form">
        <div className="input-container">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Pregunta sobre productos alemanes, locales o cualquier consulta..."
            disabled={isLoading}
          />
          <button type="submit" disabled={isLoading || !inputValue.trim()}>
            {isLoading ? "⏳" : "📤"}
          </button>
        </div>
      </form>
    </div>
  );
};

export default Chat;
