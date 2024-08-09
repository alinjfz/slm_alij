const API_BASE_URL = "http://127.0.0.1:5000/api";

// Fetch conversations
export const fetchConversations = async () => {
  const response = await fetch(`${API_BASE_URL}/conversations`, {
    method: "GET",
    credentials: "include", // Include cookies or other credentials
  });
  if (!response.ok) {
    throw new Error("Failed to load conversations");
  }
  return response.json();
};

// Send message to chat API
export const sendMessage = async (message) => {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include", // Include cookies or other credentials
    body: JSON.stringify({ message }),
  });
  if (!response.ok) {
    throw new Error("Failed to send message");
  }
  return response.json();
};

// Save a new conversation
export const saveConversation = async (conversation) => {
  const response = await fetch(`${API_BASE_URL}/conversations`, {
    method: "POST",
    credentials: "include", // Include cookies or other credentials
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(conversation),
  });
  if (!response.ok) {
    throw new Error("Failed to save conversation");
  }
  return response.json();
};

// Delete a conversation by ID
export const deleteConversation = async (id) => {
  const response = await fetch(`${API_BASE_URL}/conversations?id=${id}`, {
    method: "DELETE",
    credentials: "include", // Include cookies or other credentials
  });
  if (!response.ok) {
    throw new Error("Failed to delete conversation");
  }
  return response.json();
};
