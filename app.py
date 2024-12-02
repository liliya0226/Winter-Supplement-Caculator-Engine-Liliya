"""
Winter Supplement Calculator
Author: Liliya
----------------------------
This module calculates winter supplement amounts and processes user data 
through a Flask API and MQTT messaging system.

Main Functions:
- on_message: Handles incoming MQTT messages and processes the data.
- submit: Validates and processes input data via the `/submit` endpoint.
- get_result: Retrieves calculation results via the `/result/<topic_id>` endpoint.
"""


import json
from flask import Flask, request, jsonify
import paho.mqtt.client as mqtt
from supplement_calculator import calculate_supplement
from config import MQTT_INPUT_TOPIC_BASE, MQTT_OUTPUT_TOPIC_BASE, BROKER, PORT

# Flask App
app = Flask(__name__)

# In-memory storage for results
results = {}

# MQTT Client setup
client = mqtt.Client()

def on_message(client, userdata, msg):
    """
    Handle incoming MQTT messages.

    :param client: mqtt.Client
        The MQTT client instance.
    :param userdata:
        User-defined data (not used in this function).
    :param msg: mqtt.MQTTMessage
        The MQTT message containing a topic and payload.
    :return: None
    """
    try:
        data = json.loads(msg.payload)
        topic_id = msg.topic.split("/")[-1]
        result = calculate_supplement(data)
        results[topic_id] = result
        # Publish the result back to the output topic
        output_topic = f"{MQTT_OUTPUT_TOPIC_BASE}/{topic_id}"
        client.publish(output_topic, json.dumps(result))
    except Exception as e:
        print(f"Error processing MQTT message: {e}")

client.on_message = on_message
client.connect(BROKER, PORT)
client.loop_start()

@app.route('/submit', methods=['POST'])
def submit():
    """
    Handle data submission via the `/submit` endpoint.

    :return: Response object
        HTTP 200 with JSON: {"id": topic_id} if validation passes.
        HTTP 400 with JSON error messages if input validation fails.
    :raises KeyError:
        If required fields are missing from the input.
    """
    data = request.get_json()
    topic_id = data.get("id")

    if not topic_id:
        return jsonify({"error": "Topic ID is required"}), 400

    family_composition = data.get("familyComposition")
    if family_composition not in ["single", "couple"]:
        return jsonify({"error": "Invalid familyComposition"}), 400

    number_of_children = data.get("numberOfChildren")
    if not isinstance(number_of_children, int) or number_of_children < 0:
        return jsonify({"error": "Invalid numberOfChildren"}), 400

    family_unit_in_pay = data.get("familyUnitInPayForDecember")
    if not isinstance(family_unit_in_pay, bool):
        return jsonify({"error": "Invalid familyUnitInPayForDecember"}), 400

    # Publish input data to the MQTT input topic
    input_topic = f"{MQTT_INPUT_TOPIC_BASE}/{topic_id}"
    client.publish(input_topic, json.dumps(data))

    # Initialize the result as "pending"
    results[topic_id] = {"status": "pending"}
    return jsonify({"id": topic_id}), 200


@app.route('/result/<topic_id>', methods=['GET'])
def get_result(topic_id):
    """
    Fetch calculation result via the `/result/<topic_id>` endpoint.

    :param topic_id: str
        The unique identifier for the calculation.
    :return: Response object
        HTTP 200 with the result (JSON object). 
        If the result is not ready, returns {"status": "pending"}.
    """
    result = results.get(topic_id, {"status": "pending"})
    return jsonify(result)

if __name__ == '__main__':
    """
    Start the Flask server and MQTT client.

    :return: None
    """
    client.subscribe(f"{MQTT_OUTPUT_TOPIC_BASE}/#")
    app.run(debug=True, port=5000)
