from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

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
    "workflow2": "1200",
    "workflow3": "1204",
    "workflow4": "1206",
    "workflow5": "1208",
    "workflow6": "1210",
    "workflow7": "1212",
    "workflow8": "1214",
    "workflow9": "1216",
    "workflow10": "1218",
    "workflow11": "1294"
}

@app.route('/webhook/<workflow_name>', methods=['POST'])
def start_workflow(workflow_name):
    print("Webhook acionado!") 
    deal_ids = request.json.get('deal_ids')  

    if not deal_ids:
        return jsonify({"error": "deal_ids não fornecido"}), 400

    workflow_id = WORKFLOW_IDS.get(workflow_name)
    if not workflow_id:
        return jsonify({"error": "Workflow não encontrado"}), 404

    responses = []  
    for deal_id in deal_ids:
        array = ["crm", "CCrmDocumentDeal", f"DEAL_{deal_id}"]
        data = {
            "TEMPLATE_ID": workflow_id,
            "DOCUMENT_ID": array
        }
        print(f"Sending data to Bitrix for deal_id {deal_id}: {data}")
        try:
            response = requests.post(BITRIX_WEBHOOK_URL, json=data)
            response.raise_for_status()
            responses.append(response.json()) 
        except requests.exceptions.RequestException as e:
            print(f"Error calling Bitrix API for deal_id {deal_id}: {e}")
            responses.append({"deal_id": deal_id, "error": str(e)})

    return jsonify(responses), 200

@app.route('/webhook2/', methods=['POST'])
def start_workflow2():
    print("Webhook acionado!")
    deal_ids = request.json.get('deal_ids')  

    if not deal_ids:
        return jsonify({"error": "deal_ids não fornecido"}), 400

    workflow_name = request.json.get('workflow_name')
    workflow_id = WORKFLOW_IDS.get(workflow_name)
    if not workflow_id:
        return jsonify({"error": "Workflow não encontrado"}), 404

    responses = []  
    for deal_id in deal_ids:
        array = ["crm", "CCrmDocumentDeal", f"DEAL_{deal_id}"]
        data = {
            "TEMPLATE_ID": workflow_id,
            "DOCUMENT_ID": array
        }
        print(f"Sending data to Bitrix for deal_id {deal_id}: {data}")
        try:
            response = requests.post(BITRIX_WEBHOOK_URL, json=data)
            response.raise_for_status()
            responses.append(response.json())
        except requests.exceptions.RequestException as e:
            print(f"Error calling Bitrix API for deal_id {deal_id}: {e}")
            responses.append({"deal_id": deal_id, "error": str(e)})

    return jsonify(responses), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=97)
