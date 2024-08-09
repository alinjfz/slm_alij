import React from "react";
import PropTypes from "prop-types";

function Sidebar({
  conversations,
  onDelete,
  onSelect,
  isOpen,
  toggleSidebar,
  onNewChat,
}) {
  return (
    <div className={`sidebar ${isOpen ? "open" : "closed"}`}>
      <div className="sidebar-top-btns">
        <button className="toggle-btn" onClick={toggleSidebar}>
          <i className="bi bi-list"></i>
        </button>
        <button className="btn new-chat-btn" onClick={onNewChat}>
          + New Chat
        </button>
      </div>

      {isOpen && (
        <ul className="list-group mt-2">
          {conversations.map((conv, index) => (
            <li
              key={conv.id}
              className="list-group-item d-flex justify-content-between align-items-center"
              onClick={() => onSelect(conv.id)}
            >
              Conversation {index + 1}
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  onDelete(conv.id);
                }}
                className="btn btn-danger btn-sm"
              >
                <i className="bi bi-trash"></i>
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

Sidebar.propTypes = {
  conversations: PropTypes.array.isRequired,
  onDelete: PropTypes.func.isRequired,
  onSelect: PropTypes.func.isRequired,
  isOpen: PropTypes.bool.isRequired,
  toggleSidebar: PropTypes.func.isRequired,
};

export default Sidebar;
