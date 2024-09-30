from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
import time

app = Flask(__name__)

# Load environment variables
load_dotenv()
CODIGO_BITRIX = os.getenv('CODIGO_BITRIX')
CODIGO_BITRIX_STR = os.getenv('CODIGO_BITRIX_STR')
PROFILE = os.getenv('PROFILE')
BASE_URL_API_BITRIX = os.getenv('BASE_URL_API_BITRIX')

# Define the webhook URL
BITRIX_WEBHOOK_URL = f"{BASE_URL_API_BITRIX}/{PROFILE}/{CODIGO_BITRIX}/bizproc.workflow.start"

@app.route('/webhook/workflowone', methods=['POST'])
def workflowone():
    return start_workflow("1196")

@app.route('/webhook/workflowtwo', methods=['POST'])
def workflowtwo():
    return start_workflow("1200")

@app.route('/webhook/workflowthree', methods=['POST'])
def workflowthree():
    return start_workflow("1202")

def start_workflow(workflow_id):
    print("Webhook acionado!")  # Log to check if the endpoint is called
    deal_id = request.args.get('deal_id')
    
    if not deal_id:
        return jsonify({"error": "deal_id não fornecido"}), 400

    array = ["crm", "CCrmDocumentDeal", f"DEAL_{deal_id}"]
    data = {
        "TEMPLATE_ID": workflow_id,
        "DOCUMENT_ID": array
    }

    # Optional: Log the data being sent to Bitrix for debugging
    print(f"Sending data to Bitrix: {data}")

    time.sleep(10)  # Consider removing or reducing this in production
    try:
        response = requests.post(BITRIX_WEBHOOK_URL, json=data)
        response.raise_for_status()  # Raise an error for bad responses
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        print(f"Error calling Bitrix API: {e}")
        return jsonify({"error": "Failed to start workflow", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9997)
