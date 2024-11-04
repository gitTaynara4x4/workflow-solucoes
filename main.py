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
    "workflow1": "1196", #primeiro boleto(1.1)
    "workflow2": "1200", #primeiro boleto(1.2)
    "workflow3": "1204", #segundo boleto(1.1)
    "workflow4": "1206", #segundo boleto(1.2)
    "workflow5": "1208", #terceiro boleto(1.1)
    "workflow6": "1210", #terceiro boleto(1.2)
    "workflow7": "1212", #quarto boleto(1.1)
    "workflow8": "1214", #quarto boleto(1.2)
    "workflow9": "1216", #quinto boleto(1.1)
    "workflow10": "1218", #quinto boleto(1.2)
    "workflow11": "1314", #workflow para o site
    "workflow12": "1294", #workflow para a fila de ativos
    "workflow13": "1390" #workflow para campo sem fuso horario ser atualizado. 
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
    app.run(host='0.0.0.0', port=97)
