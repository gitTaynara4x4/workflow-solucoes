from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)

BITRIX_WEBHOOK_URL = "https://marketingsolucoes.bitrix24.com.br/rest/35002/7a2nuej815yjx5bg/bizproc.workflow.start"

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
    print("Webhook acionado!")  # Log para verificar se o endpoint está sendo chamado
    deal_id = request.args.get('deal_id')
    if not deal_id:
        return jsonify({"error": "deal_id não fornecido"}), 400

    array = ["crm", "CCrmDocumentDeal", f"DEAL_{deal_id}"]
    data = {
        "TEMPLATE_ID": workflow_id,
        "DOCUMENT_ID": array
    }

    time.sleep(10)
    response = requests.post(BITRIX_WEBHOOK_URL, json=data)
    
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7072)
