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

### Usage: Backend-Frontend Interaction

The backend simplifies integration with frontend systems through its REST API.

- **Submit Data**: Frontend sends family data using a **POST** request to `/submit`, triggering the supplement calculation.
- **Fetch Results**: Results are retrieved via a **GET** request to `/result/<topic_id>`.


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
## Testing
Tests are implemented using the `unittest` framework. To execute them, run:

```bash
python -m unittest test_rules_engine
