from flask import Blueprint, request, jsonify
import json
import os

main = Blueprint('main', __name__)

CONVERSATIONS_FILE = os.path.join('back', 'static', 'conversations.json')

@main.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    # Handle chat logic here (e.g., call an AI model)
    response = {"message": f"Echo: {data['message']}"}
    return jsonify(response)

@main.route('/api/conversations', methods=['GET'])
def get_conversations():
    with open(CONVERSATIONS_FILE, 'r') as file:
        conversations = json.load(file)
    return jsonify(conversations)

@main.route('/api/conversations', methods=['POST'])
def add_conversation():
    conversation = request.json
    with open(CONVERSATIONS_FILE, 'r+') as file:
        conversations = json.load(file)
        conversations.append(conversation)
        file.seek(0)
        json.dump(conversations, file)
    return jsonify({"status": "Conversation added"}), 201

@main.route('/api/conversations', methods=['DELETE'])
def delete_conversation():
    conversation_id = request.args.get('id')
    with open(CONVERSATIONS_FILE, 'r+') as file:
        conversations = json.load(file)
        conversations = [c for c in conversations if c['id'] != conversation_id]
        file.seek(0)
        file.truncate()
        json.dump(conversations, file)
    return jsonify({"status": "Conversation deleted"}), 200
