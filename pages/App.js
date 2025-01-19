// Import required libraries
import React, { useState, useEffect } from 'react';
import './App.css'; // Add CSS for styling the rectangles

function App() {
  const [conversation, setConversation] = useState({
    transcriptions: [],
    translations: []
  });
  const [input, setInput] = useState('');

  useEffect(() => {
    // Simulate data flow from the Python backend (replace this with actual API calls)
    const fetchConversation = async () => {
      // Mock data from main.py
      const transcribedText = 'Hello, how are you?';
      const englishResponse = 'I am fine, thank you!';
      const inputTranslation = '你好，你好吗？';
      const languageResponse = '我很好，谢谢！';

      setConversation(prev => ({
        transcriptions: [...prev.transcriptions, { transcribedText, englishResponse }],
        translations: [...prev.translations, { inputTranslation, languageResponse }]
      }));
    };

    const interval = setInterval(fetchConversation, 5000); // Simulate continuous data fetch
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="App">
      <div className="conversation-container">
        <div className="message-group">
          <h3>Transcriptions and Responses</h3>
          {conversation.transcriptions.map((item, index) => (
            <div key={index} className="message-box">
              <p><strong>Transcribed:</strong> {item.transcribedText}</p>
              <p><strong>English Response:</strong> {item.englishResponse}</p>
            </div>
          ))}
        </div>
        <div className="message-group">
          <h3>Translations and Responses</h3>
          {conversation.translations.map((item, index) => (
            <div key={index} className="message-box">
              <p><strong>Input Translation:</strong> {item.inputTranslation}</p>
              <p><strong>Language Response:</strong> {item.languageResponse}</p>
            </div>
          ))}
        </div>
      </div>
      <div className="input-container">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message here..."
        />
        <button onClick={() => console.log('Sending message:', input)}>Send</button>
      </div>
    </div>
  );
}

export default App;

// App.css
