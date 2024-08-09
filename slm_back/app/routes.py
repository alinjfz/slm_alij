from flask import Blueprint, request, jsonify
import requests
import json
import os
import httpx
from openai import OpenAI
# import openai
import logging

main = Blueprint('main', __name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONVERSATIONS_FILE = os.path.join(BASE_DIR, 'static', 'conversations.json')

EXTERNAL_API_URL = "http://0.0.0.0:11434/api/chat"

def llama3_another_way(prompt):
    return ""
    # params = {
    #     "model": "llama3.1:8b",
    #     "message": "why is the sky blue?",
    #     "stream": "False"
    # }

    # response = httpx.get(EXTERNAL_API_URL, params=params)

    # if response.status_code == 200:
    #     print(response.json())
    # else:
    #     print(f"Error: {response.status_code}")
    # data = {
    #     "model": "llama3.1:8b",
    #     "messages": [
    #         {
    #           "role": "user",
    #           "content": prompt
    #         }
    #     ],
    #     "stream": False,
    # }

    # headers = {
    #     'Content-Type': 'application/json'
    # }
    
    # try:
    #     # Making a POST request with httpx
    #     response = httpx.post(EXTERNAL_API_URL, headers=headers, json=data)
        
    #     # Check if the response status code indicates an error
    #     response.raise_for_status()
        
    #     # Parse the JSON response
    #     return response.json().get('message', {}).get('content', None)
    # except httpx.HTTPStatusError as e:
    #     print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
    # except Exception as e:
    #     print(f"An error occurred: {str(e)}")
    # return None

def call_llama3_openai_api(user_message):
    # logging.basicConfig(level=logging.ERROR)
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
    sample_output= {
        "model":"llama3.1:8b",
        "created_at":"2024-08-09T10:45:30.480353Z",
        "message": {
            "role":"assistant",
            "content":"The sky appears blue to us because of a phenomenon called scattering."
        },
        "done_reason":"stop",
        "done":True,
        "total_duration":"12339774584",
        "load_duration":"38116625",
        "prompt_eval_count":"17",
        "prompt_eval_duration":"158251000",
        "eval_count":"401",
        "eval_duration":"12142026000",
    }
    data = {
        "model": "llama3.1:8b",
        "messages": [
            {
              "role": "user",
              "content": prompt
            }
        ],
        "stream": False,        
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(EXTERNAL_API_URL, headers=headers, data=json.dumps(data))
    # Check if the response status code indicates an error
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        print(response.text)
        return None
    return response.json().get('message', {}).get('content', None)
    #   response = requests.post(EXTERNAL_API_URL, headers=headers, json=data)  
    # print("resss",response.message)
    # return "Hi"
    # return response.json()
    # return response.json()#['message']['content']
    # from langchain_community.chat_models import ChatOllama

    # llm = ChatOllama(model="llama3", temperature=0)
    # response = llm.invoke("who wrote the book godfather?")
    # print(response.content)

def call_llama_my_way(prompt):
    return ""
    # response = requests.post("http://0.0.0.0:11434/api/chat",json={"model": "llama3.1:8b", "messages": prompt, "stream": False})
    # if response.status_code != 200:
    #         print(f"Error: Received status code {response.status_code}")
    #         print(response.text)
    #         return None
    # return response.json().get('message', {}).get('content', None)
    # sample_output= {
    #     "message": {
    #         "content":"The sky appears blue to us because of a phenomenon called scattering."
    #     },
    # }
    # the_api_url= "http://0.0.0.0:11434/api/generate"
    # data = {
    #     "model": "llama3.1:8b",
    #     "prompt":prompt,
    #     "stream": False,        
    #     "format": "json",
    # }
    # headers = {
    #     'Content-Type': 'application/json'
    # }
    # response = requests.post(the_api_url, data=data)
    # # Check if the response status code indicates an error
    # if response.status_code != 200:
    #     print(f"Error: Received status code {response.status_code}")
    #     print(response.text)
    #     return None
    # return response.json().get('message', {}).get('content', None)

    # client = OpenAI(
    #     base_url='http://localhost:11434/v1/',
    #     # required but ignored
    #     api_key='ollama',
    # )
    # try:
    #     chat_completion = client.chat.completions.create(
    #         messages=[
    #             {
    #                 'role': 'user',
    #                 'content': 'Say this is a test',
    #             }
    #         ],
    #         model='llama3.1:8b',
    #     )
    #     print(chat_completion)
    # except Exception as e:
    #     print(e)
    # return ""
    # completion = client.completions.create(
    #     model="llama3",
    #     prompt="Say this is a test",
    # )

    # list_completion = client.models.list()

    # model = client.models.retrieve("llama3")

    # embeddings = client.embeddings.create(
    #     model="all-minilm",
    #     input=["why is the sky blue?", "why is the grass green?"],
    # )

@main.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data['message']
    
    # Call the external API
    bot_response = call_llama3_api(user_message)
    # bot_response = call_llama3_openai_api(user_message)
    return jsonify({"message": bot_response})

def load_conversations():
    if not os.path.exists(CONVERSATIONS_FILE):
        return []
    with open(CONVERSATIONS_FILE, 'r') as file:
        return json.load(file)

def save_conversations(conversations):
    with open(CONVERSATIONS_FILE, 'w') as file:
        json.dump(conversations, file, indent=4)

@main.route('/api/conversations', methods=['GET'])
def get_conversations():
    conversations = load_conversations()
    return jsonify(conversations)

@main.route('/api/conversations', methods=['POST'])
def save_conversation():
    new_conversation = request.json
    conversations = load_conversations()
    existing_conversation = next((c for c in conversations if c['id'] == new_conversation['id']), None)
    
    if existing_conversation:
        existing_conversation['conversation'] = new_conversation['conversation']
    else:
        conversations.append(new_conversation)
    
    save_conversations(conversations)
    return jsonify(new_conversation)

@main.route('/api/conversations', methods=['DELETE'])
def delete_conversation():
    conversation_id = request.args.get('id')
    conversations = load_conversations()
    conversations = [c for c in conversations if c['id'] != conversation_id]
    save_conversations(conversations)
    return jsonify({'success': True})
