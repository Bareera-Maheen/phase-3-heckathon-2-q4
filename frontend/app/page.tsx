'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';
import { Send, User, Bot, Plus } from 'lucide-react';

export default function Home() {
  const [messages, setMessages] = useState<{ role: string; content: string }[]>([]);
  const [input, setInput] = useState('');
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [userId, setUserId] = useState('demo-user-123'); // Demo user

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages([...messages, userMessage]);
    setInput('');

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await axios.post(`${apiUrl}/api/${userId}/chat`, {
        message: input,
        conversation_id: conversationId,
      }, {
        headers: { 'user-id': userId }
      });

      const assistantMessage = { role: 'assistant', content: response.data.response };
      setMessages(prev => [...prev, assistantMessage]);
      setConversationId(response.data.conversation_id);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [...prev, { role: 'assistant', content: 'Sorry, I encountered an error.' }]);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50 text-black">
      <header className="p-4 bg-white border-b flex justify-between items-center">
        <h1 className="text-xl font-bold">Todo AI Chatbot</h1>
        <button 
          onClick={() => { setMessages([]); setConversationId(null); }}
          className="p-2 hover:bg-gray-100 rounded-full"
        >
          <Plus size={20} />
        </button>
      </header>

      <main className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[80%] p-3 rounded-lg flex items-start space-x-2 ${
              msg.role === 'user' ? 'bg-blue-600 text-white' : 'bg-white border'
            }`}>
              {msg.role === 'assistant' && <Bot size={18} className="mt-1" />}
              <p>{msg.content}</p>
              {msg.role === 'user' && <User size={18} className="mt-1" />}
            </div>
          </div>
        ))}
      </main>

      <footer className="p-4 bg-white border-t">
        <div className="max-w-4xl mx-auto flex space-x-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Type your message..."
            className="flex-1 p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={sendMessage}
            className="p-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            <Send size={20} />
          </button>
        </div>
      </footer>
    </div>
  );
}
