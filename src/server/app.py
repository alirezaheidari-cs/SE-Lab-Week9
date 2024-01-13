from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

MICROSERVICE_BASE_URL = "http://nginx:80"


@app.route('/student', methods=['POST', 'GET', 'PUT', 'DELETE'])
def student():
    microservice_url = f"{MICROSERVICE_BASE_URL}/student"
    response = requests.request(
        method=request.method,
        url=microservice_url,
        json=request.json,
        params=request.args
    )

    return jsonify(response.json()), response.status_code


@app.route('/students', methods=['GET'])
def all_students():
    response = requests.get(f"{MICROSERVICE_BASE_URL}/students")
    return jsonify(response.json()), response.status_code


if __name__ == '__main__':
    app.run(debug=True, port=4000)
