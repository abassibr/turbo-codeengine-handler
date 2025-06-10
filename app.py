import os
import logging
from flask import Flask, request, jsonify
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

TURBOHOST = os.environ['TURBOHOST']
TURBOUSER = os.environ['TURBOUSER']
TURBOPASS = os.environ['TURBOPASS']

PRE_APPROVED_GROUP_ID = os.environ['PRE_APPROVED_GROUP_ID']
APPROVED_GROUP_ID = os.environ['APPROVED_GROUP_ID']

def login(session):
    login_url = f"{TURBOHOST}/api/v3/login"
    logger.info(f"Logging in to {login_url} with user {TURBOUSER}")
    resp = session.post(login_url, data={"username": TURBOUSER, "password": TURBOPASS})
    resp.raise_for_status()
    logger.info("Login successful")

def get_group_members(session, group_id):
    url = f"{TURBOHOST}/vmturbo/rest/groups/{group_id}"
    resp = session.get(url)
    resp.raise_for_status()
    group_data = resp.json()
    members = group_data.get("memberUuidList", [])
    logger.info(f"Group {group_id} has {len(members)} members")
    return members

def update_group_members(session, group_id, members):
    url = f"{TURBOHOST}/vmturbo/rest/groups/{group_id}/members"
    resp = session.put(url, json=members)
    resp.raise_for_status()
    logger.info(f"Updated group {group_id} members successfully")
    return resp.json()

@app.route('/update_entity_group', methods=['POST'])
def update_entity_group():
    data = request.get_json()
    if not data or 'entity_uuid' not in data:
        return jsonify({"error": "Missing 'entity_uuid' in request body"}), 400

    entity_uuid = data['entity_uuid']
    with requests.Session() as session:
        try:
            login(session)

            pre_members = get_group_members(session, PRE_APPROVED_GROUP_ID)
            if entity_uuid in pre_members:
                pre_members.remove(entity_uuid)
                update_group_members(session, PRE_APPROVED_GROUP_ID, pre_members)
            else:
                logger.info(f"Entity {entity_uuid} not in pre-approved group")

            approved_members = get_group_members(session, APPROVED_GROUP_ID)
            if entity_uuid not in approved_members:
                approved_members.append(entity_uuid)
                update_group_members(session, APPROVED_GROUP_ID, approved_members)
            else:
                logger.info(f"Entity {entity_uuid} already in approved group")

            return jsonify({"status": "success", "message": f"Entity {entity_uuid} moved successfully"}), 200

        except requests.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            return jsonify({"error": str(e)}), 500
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
