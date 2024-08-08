from flask import Blueprint, request, jsonify
import requests
import json
import os

main = Blueprint('main', __name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONVERSATIONS_FILE = os.path.join(BASE_DIR, 'static', 'conversations.json')

EXTERNAL_API_URL = "http://localhost:11434/api/chat"

import openai
import logging

logging.basicConfig(level=logging.ERROR)

def call_llama3_openai_api(user_message):
    try:
        client = openai.OpenAI(
        base_url="http://localhost:11434/api/chat",
        api_key="nokeyneeded",
        )
        response = client.chat.completions.create(
            model="llama3.1:8b",
            temperature=0.7,
            n=1,
            messages=[{"role": "user", "content": user_message}]
        )
        return response
    # except openai.error.OpenAIError as e:
    #     logging.error(f"OpenAI API error: {e}")
    #     # Handle specific errors or re-raise if necessary
    #     raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise

def call_llama3_api(prompt):
    data = {
        "model": "llama3.1:8b",
        "messages": [
            {
              "role": "user",
              "content": prompt
            }
        ],
        "stream": False
    }
    
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(EXTERNAL_API_URL, headers=headers, json=data)  
    print(response)
    return "Hi"
    # return response.json()
    # return response.json()#['message']['content']
    # from langchain_community.chat_models import ChatOllama

    # llm = ChatOllama(model="llama3", temperature=0)
    # response = llm.invoke("who wrote the book godfather?")
    # print(response.content)

@main.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data['message']
    
    # Call the external API
    bot_response = call_llama3_api(user_message)
    # bot_response = call_llama3_openai_api(user_message)
    return jsonify({"message": bot_response})

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
