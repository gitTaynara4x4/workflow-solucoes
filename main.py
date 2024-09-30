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

WORKFLOW_IDS = {
    "workflow1": "1196",
    "workflow2": "1196",
    "workflow3": "1196",
    "workflow4": "1196",
    "workflow5": "1196",
    "workflow6": "1196",
    "workflow7": "1196",
    "workflow8": "1196",
    "workflow9": "1196",
    "workflow10": "1200"
}

@app.route('/webhook/<workflow_name>', methods=['POST'])
def start_workflow(workflow_name):
    print("Webhook acionado!")  # Log to check if the endpoint is called
    deal_id = request.args.get('deal_id')

    if not deal_id:
        return jsonify({"error": "deal_id não fornecido"}), 400

    # Get the workflow ID from the dictionary
    workflow_id = WORKFLOW_IDS.get(workflow_name)
    if not workflow_id:
        return jsonify({"error": "Workflow não encontrado"}), 404

    array = ["crm", "CCrmDocumentDeal", f"DEAL_{deal_id}"]
    data = {
        "TEMPLATE_ID": workflow_id,
        "DOCUMENT_ID": array
    }

    # Log the data being sent to Bitrix for debugging
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
