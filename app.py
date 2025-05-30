from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST'])
def handle_event():
    data = request.json
    print("Received event:", data)

    # TODO: Call Turbo API to move entity to approved group
    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
