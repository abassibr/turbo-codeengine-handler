import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

TURBOHOST = os.getenv('TURBOHOST')
TURBOUSER = os.getenv('TURBOUSER')
TURBOPASS = os.getenv('TURBOPASS')
PRE_APPROVED_GROUP_ID = os.getenv('PRE_APPROVED_GROUP_ID')
APPROVED_GROUP_ID = os.getenv('APPROVED_GROUP_ID')

def modify_entity_groups(entity_uuid):
    auth = (TURBOUSER, TURBOPASS)

    # Remove entity from Pre-Approved Group
    remove_url = f"{TURBOHOST}/api/groups/{PRE_APPROVED_GROUP_ID}/entities/{entity_uuid}"
    print(f"Calling DELETE: {remove_url}")
    remove_resp = requests.delete(remove_url, auth=auth)
    print("Remove response:", remove_resp.status_code, remove_resp.text)

    if remove_resp.status_code not in [200, 204]:
        return remove_resp.status_code, f"Failed to remove entity from Pre-Approved Group: {remove_resp.text}"

    # Add entity to Approved Group
    add_url = f"{TURBOHOST}/api/groups/{APPROVED_GROUP_ID}/entities"
    add_payload = {"entityIds": [entity_uuid]}
    print(f"Calling POST: {add_url} with payload: {add_payload}")
    add_resp = requests.post(add_url, auth=auth, json=add_payload)
    print("Add response:", add_resp.status_code, add_resp.text)

    if add_resp.status_code not in [200, 204]:
        return add_resp.status_code, f"Failed to add entity to Approved Group: {add_resp.text}"

    return 200, "Entity moved successfully"


@app.route('/', methods=['POST'])
def handle_event():
    data = request.json
    print("Received event:", data)

    # Check if action is approve
    if data.get('action') != 'approve':
        return jsonify({"message": "Action not approved, ignoring."}), 200

    entity_uuid = data.get('entity_uuid')
    if not entity_uuid:
        return jsonify({"error": "No entity_uuid found"}), 400

    status, msg = modify_entity_groups(entity_uuid)
    return jsonify({"status_code": status, "message": msg}), status

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
