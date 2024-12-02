# Winter-Supplement-Caculator-Engine-Liliya


## Overview

The **Winter Supplement Calculator API** is a Flask-based web application designed to compute winter supplement amounts for families. It integrates MQTT for message passing and provides a REST API for user interaction. The application ensures a robust workflow for submitting family data, processing calculations, and retrieving results.

---

### Key Features

- **Family Supplement Calculator**: Dynamically computes supplement amounts based on family type and number of children.
- **REST API Endpoints**:
  - **POST `/submit`**: Accepts family data in JSON format to trigger calculations.
  - **GET `/result/<topic_id>`**: Fetches calculated results for a specific `topic_id`.
- **MQTT Integration**: Publishes and subscribes to data topics, enabling real-time data processing.
- **Input Validation**: Ensures all input data is valid and provides clear error messages for issues.
- **Extensibility**: Designed for easy customization and integration with additional services or platforms.

---

## Workflow

This application processes family supplement data through a Flask backend with MQTT for communication. Below is the step-by-step process:

1. **Submit Data**  
   Clients send family data via the `/submit` POST endpoint.

2. **Data Validation**  
   Flask validates the submitted data to ensure it meets the required format and rules (e.g., valid family composition, non-negative number of children).

3. **Publish to MQTT Input Topic**  
   The validated data is published to the MQTT input topic:  
   `BRE/calculateWinterSupplementInput/<topic_id>`.

4. **Process Data via MQTT**  
   The Flask application's MQTT client listens to the input topic, retrieves the published data, and prepares it for calculation.

5. **Calculate Results**  
   The backend processes the data using the `calculate_supplement` function, determining the supplement based on eligibility and family structure.

6. **Publish Results to MQTT Output Topic**  
   The calculated results are published to an MQTT output topic:  
   `BRE/calculateWinterSupplementOutput/<topic_id>` and stored in the `results` dictionary.

7. **Query Results**  
   Clients fetch the results using the `/result/<topic_id>` GET endpoint.

## Prerequisites

Before you start, ensure the following tools are installed:

- Python 3.8 or above
- `pip` (Python package installer)

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/liliya0226/Winter-Supplement-Caculator-Engine-Liliya.git
   cd Winter-Supplement-Calculator-Engine-Liliya
2. Give execution permission to set.sh:
    ```bash
    chmod +x set.sh
3. Run the Setup Script: Create a virtual environment and install dependencies.
    ```bash
    ./set.sh
3. ### Activate the virtual environment (if not already activated):

- **On Linux/MacOS**:
  ```bash
  source venv/bin/activate
- **On Windows**:
  ```bash
  venv\Scripts\activate
4. Run the Application: Start the Flask API and MQTT client.
    ```bash
    python3 app.py
5. Submit Data: Use a tool like curl or Postman to send a POST request to the /submit endpoint. For example:
    ```bash
    curl -X POST http://127.0.0.1:5000/submit -H "Content-Type: application/json" -d '{"id": <MQTT topic ID>", "numberOfChildren": 2, "familyComposition": "couple", "familyUnitInPayForDecember": true}'
6. Retrieve Results: Use a GET request to retrieve the calculation results.
    ```bash
    curl http://127.0.0.1:5000/result/<MQTT topic ID>
## MQTT Configuration

All MQTT settings, including broker details and topic configurations, are managed in the `config.py` file.

### How to Configure MQTT Topics

Open the `config.py` file, update MQTT_INPUT_TOPIC_BASE to your desired input topic, update MQTT_OUTPUT_TOPIC_BASE to your desired output topic.
   ```python
   # config.py

   # MQTT Broker configuration
   BROKER = "test.mosquitto.org"
   PORT = 1883

   # MQTT Topic Configuration
   MQTT_INPUT_TOPIC_BASE = "BRE/calculateWinterSupplementInput"
   MQTT_OUTPUT_TOPIC_BASE = "BRE/calculateWinterSupplementOutput"
## Testing
Tests are implemented using the `unittest` framework. To execute them, run:

```bash
python -m unittest test_rules_engine
