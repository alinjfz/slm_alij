import React from "react";
import PropTypes from "prop-types";

function ConversationList({ conversations, onDelete }) {
  return (
    <ul className="list-group">
      {conversations.map((conv, index) => (
        <li
          key={index}
          className="list-group-item d-flex justify-content-between align-items-center"
        >
          Conversation {index + 1}
          <button
            onClick={() => onDelete(conv.id)}
            className="btn btn-danger btn-sm"
          >
            Delete
          </button>
        </li>
      ))}
    </ul>
  );
}

ConversationList.propTypes = {
  conversations: PropTypes.array.isRequired,
  onDelete: PropTypes.func.isRequired,
};

export default ConversationList;
