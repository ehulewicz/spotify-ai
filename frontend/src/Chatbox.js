import React, { useState, useRef, useEffect } from 'react';

import './global.css';

const Chatbox = () => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const textareaRef = useRef(null);

  const [test, setTest] = useState('');

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [input]);

  const handleKeyDown = (e) => {
    if (e.shiftKey && e.key === 'Enter') {
      e.preventDefault();
      setInput((prevInput) => prevInput + '\n');
    } else if (e.key === 'Enter') {
      setTest('Awating response...');
      e.preventDefault();
      handleSend();
    }
  }

  const handleSend = async () => {
    if (!input.trim()) return;
  
    const userMessage = { sender: 'user', text: input };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInput('');
  
    try {
        // ${window.location.hostname} only matters if going to containerize web browser (backend instead of localhost)
        const response = await fetch(`http://${window.location.hostname}:5001/gpt/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: input }),
      });
      
      const data = await response.json();
      setTest('Message received successfully')
      setTest(`http://${window.location.hostname}:5001/gpt/`);
      
      const gptMessage = { sender: 'gpt', text: data.response };
      setMessages((prevMessages) => [...prevMessages, gptMessage]);
    } catch (error) {
      setTest('' + error);
      setTest(`http://${window.location.hostname}:5001/gpt/` + '\n' + error);
    }
  };

  return (
    <div className="chatbox">
      <div className="messages">
        {messages.map((message, index) => (
          <div key={index} className={message.sender === 'user' ? 'user-message' : 'gpt-message'}>
            {message.text}
          </div>
        ))}
      </div>  
      <div className="input-container">
        <textarea
          ref={textareaRef}
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type your message..."
        />
        <button onClick={handleSend}>Send</button>
      </div>
      <div className="development">
        <pre>{test}</pre>
      </div>
    </div>
  );
}

export default Chatbox;