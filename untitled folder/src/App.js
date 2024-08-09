import React, { useState, useEffect } from "react";
import Sidebar from "./components/Sidebar";
import ChatBox from "./components/ChatBox";
import ErrorAlert from "./components/ErrorAlert";
import {
  fetchConversations,
  sendMessage,
  saveConversation,
  deleteConversation,
} from "./services/apiService";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";

function App() {
  const [message, setMessage] = useState("");
  const [conversation, setConversation] = useState([]);
  const [conversations, setConversations] = useState([]);
  const [error, setError] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [selectedConversationId, setSelectedConversationId] = useState(null);

  useEffect(() => {
    const loadConversations = async () => {
      try {
        const data = await fetchConversations();
        setConversations(data);
        if (data.length > 0) {
          const lastConversation = data[data.length - 1];
          setSelectedConversationId(lastConversation.id);
          setConversation(lastConversation.conversation);
        }
      } catch (err) {
        setError(err.message);
      }
    };

    loadConversations();
  }, []);

  const handleSendMessage = async () => {
    try {
      const response = await sendMessage(message);
      const newMessage = { message, response: response.message };
      const updatedConversation = [...conversation, newMessage];
      setConversation(updatedConversation);
      setMessage("");

      // Automatically save the conversation
      if (selectedConversationId) {
        const updatedConversations = conversations.map((conv) =>
          conv.id === selectedConversationId
            ? { ...conv, conversation: updatedConversation }
            : conv
        );
        setConversations(updatedConversations);
      } else {
        const newConversation = {
          id: Date.now(),
          conversation: updatedConversation,
        };
        await saveConversation(newConversation);
        setConversations([...conversations, newConversation]);
        setSelectedConversationId(newConversation.id);
      }
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDeleteConversation = async (id) => {
    try {
      await deleteConversation(id);
      const remainingConversations = conversations.filter((c) => c.id !== id);
      setConversations(remainingConversations);
      if (id === selectedConversationId) {
        if (remainingConversations.length > 0) {
          const lastConversation =
            remainingConversations[remainingConversations.length - 1];
          setSelectedConversationId(lastConversation.id);
          setConversation(lastConversation.conversation);
        } else {
          setConversation([]);
          setSelectedConversationId(null);
        }
      }
    } catch (err) {
      setError(err.message);
    }
  };

  const handleSelectConversation = (id) => {
    const selectedConversation = conversations.find((c) => c.id === id);
    setConversation(selectedConversation.conversation);
    setSelectedConversationId(id);
  };

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  const clearError = () => {
    setError(null);
  };

  return (
    <div className="app-container">
      <Sidebar
        conversations={conversations}
        onDelete={handleDeleteConversation}
        onSelect={handleSelectConversation}
        isOpen={sidebarOpen}
        toggleSidebar={toggleSidebar}
      />
      <div className={`chat-section ${sidebarOpen ? "with-sidebar" : ""}`}>
        <ErrorAlert error={error} clearError={clearError} />
        <ChatBox
          conversation={conversation}
          message={message}
          setMessage={setMessage}
          handleSendMessage={handleSendMessage}
        />
      </div>
    </div>
  );
}
export default App;
