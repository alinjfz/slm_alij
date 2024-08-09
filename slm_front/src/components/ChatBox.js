import React, { useState } from "react";
import "./ChatBox.css";

const ChatBox = ({ conversation, message, setMessage, handleSendMessage }) => {
  const [loading, setLoading] = useState(false);

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !loading) {
      onSendMessage();
    }
  };

  const onSendMessage = async () => {
    setLoading(true);
    await handleSendMessage();
    setLoading(false);
  };

  const parseText = (text) => {
    // Handling code blocks first and storing them temporarily
    const codeBlocks = [];
    text = text.replace(/```(.*?)\n([\s\S]*?)```/g, (match, p1, p2, offset) => {
      const placeholder = `CODEBLOCK_PLACEHOLDER_${codeBlocks.length}`;
      codeBlocks.push(`<pre><code>${p2}</code></pre>`);
      return placeholder;
    });

    // Then handle inline code
    text = text.replace(/`([^`]+)`/g, "<code>$1</code>");

    // Handling headings (#, ##)
    text = text.replace(/^### (.*$)/gim, "<h3>$1</h3>");
    text = text.replace(/^## (.*$)/gim, "<h2>$1</h2>");
    text = text.replace(/^# (.*$)/gim, "<h1>$1</h1>");

    // Handling bold (**text**)
    text = text.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");

    // Handling line breaks
    text = text.replace(/\n/g, "<br/>");

    // Replacing code block placeholders with the actual code blocks
    codeBlocks.forEach((codeBlock, index) => {
      text = text.replace(`CODEBLOCK_PLACEHOLDER_${index}`, codeBlock);
    });

    return text;
  };

  return (
    <div className="chatbox-container">
      <div className="messages-container">
        {conversation.map((msg, index) => (
          <React.Fragment key={index}>
            {msg.message && (
              <div className="message-wrapper sent">
                <div className="message sent-message">{msg.message}</div>
              </div>
            )}
            {msg.response && (
              <div className="message-wrapper received">
                <div
                  className="message received-message"
                  dangerouslySetInnerHTML={{
                    __html: parseText(msg.response),
                  }}
                ></div>
              </div>
            )}
          </React.Fragment>
        ))}
        {loading && (
          <div className="loading-indicator">
            <div
              className="spinner-grow spinner-grow-sm text-dark"
              role="status"
            >
              <span className="sr-only"></span>
            </div>
          </div>
        )}
      </div>
      <div className="input-container">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type a message..."
          className="message-input"
          disabled={loading}
        />
        <button
          onClick={onSendMessage}
          className="send-button"
          disabled={loading}
        >
          {loading ? (
            <div
              className="spinner-border spinner-border-sm text-light"
              role="status"
            >
              <span className="sr-only"></span>
            </div>
          ) : (
            <span>&#9654;</span>
          )}
        </button>
      </div>
    </div>
  );
};

export default ChatBox;
