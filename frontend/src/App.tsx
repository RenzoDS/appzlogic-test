import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Container, Card, Form, Button } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

type Message = {
  id: number;
  text: string;
  sender: 'user' | 'bot';
};

const App: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  // Scroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage: Message = {
      id: Date.now(),
      text: input,
      sender: 'user',
    };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const res = await axios.post('http://localhost:8000/api/chat', { message: userMessage.text });
      const botMessage: Message = {
        id: Date.now() + 1,
        text: res.data.response,
        sender: 'bot',
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error(error);
      const errorMessage: Message = {
        id: Date.now() + 2,
        text: 'Error occurred. Please try again.',
        sender: 'bot',
      };
      setMessages((prev) => [...prev, errorMessage]);
    }
    setLoading(false);
  };

  return (
    <Container
      fluid
      className="d-flex justify-content-center align-items-center"
      style={{ minHeight: '100vh', backgroundColor: '#f0f2f5' }}
    >
      <Card style={{ width: '100%', maxWidth: '500px' }}>
        <Card.Header as="h5" className="text-center">
          Chat App
        </Card.Header>
        <Card.Body className="d-flex flex-column p-0" style={{ height: '70vh' }}>
          {/* Chat Messages Area */}
          <div style={{ flex: 1, overflowY: 'auto', padding: '1rem', backgroundColor: '#e5ddd5' }}>
            {messages.map((msg) => (
              <div key={msg.id} className={`mb-2 d-flex ${msg.sender === 'user' ? 'justify-content-end' : 'justify-content-start'}`}>
                <span
                  className={`p-2 rounded ${msg.sender === 'user' ? 'bg-primary text-white' : 'bg-light text-dark'}`}
                  style={{ maxWidth: '80%' }}
                >
                  {msg.text}
                </span>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          {/* Message Input Area */}
          <Form onSubmit={handleSend} className="d-flex border-top p-2">
            <Form.Control
              type="text"
              placeholder="Type your message..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={loading}
            />
            <Button variant="primary" type="submit" disabled={loading} className="ms-2">
              {loading ? 'Sending...' : 'Send'}
            </Button>
          </Form>
        </Card.Body>
      </Card>
    </Container>
  );
};

export default App;
