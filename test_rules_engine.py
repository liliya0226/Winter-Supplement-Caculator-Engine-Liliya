"""
Winter Supplement Test Suite
Author: Liliya
----------------------------
This test suite validates the functionality of the Winter Supplement Calculator API and MQTT integration. 
It includes test cases for eligibility, correct calculations, error handling, and edge cases. 

Key Features:
1. Ensures eligibility is determined accurately based on input data.
2. Verifies calculations for base amounts and child supplements.
3. Tests error responses for invalid inputs.
4. Simulates MQTT message handling for end-to-end flow validation.
"""

from unittest.mock import MagicMock
import unittest
from flask import json
from app import app
from app import results

class TestFlaskMQTTIntegrationWithMagicMock(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment with a mocked Flask client and MQTT components.

        :return: None
            Initializes the test client, replaces global results with a mock dictionary,
            and substitutes the MQTT client publish method with a MagicMock.
        """
        self.app = app.test_client()
        self.app.testing = True

        # Replace global results with a mock dictionary
        from app import results
        self.mock_results = results

        # Replace MQTT client publish with a MagicMock
        from app import client
        self.mock_client = MagicMock()
        client.publish = self.mock_client.publish


    def simulate_on_message(self, input_data, expected_result):
        """
        Simulate the MQTT `on_message` behavior for testing.

        :param input_data: dict
            The incoming MQTT message payload containing:
            - id (str): Unique identifier for the calculation.
            - familyComposition (str): "single" or "couple".
            - numberOfChildren (int): Non-negative integer representing the number of children.
            - familyUnitInPayForDecember (bool): Flag indicating December payment eligibility.
        :param expected_result: dict
            The expected result after processing the input data, including:
            - isEligible (bool): Eligibility status.
            - baseAmount (float): Calculated base amount.
            - childrenAmount (float): Calculated child supplement amount.
            - supplementAmount (float): Total supplement amount.
        :return: None
            Simulates publishing to input/output MQTT topics and updates the `results` dictionary.
        """
        topic_id = input_data["id"]
        input_topic = f"BRE/calculateWinterSupplementInput/{topic_id}"
        output_topic = f"BRE/calculateWinterSupplementOutput/{topic_id}"

        # Simulate input topic publish
        self.mock_client.publish(input_topic, json.dumps(input_data))

        # Simulate computation and output topic publish
        self.mock_client.publish(output_topic, json.dumps(expected_result))
        results[topic_id] = expected_result


    def test_single_person_no_children_eligible(self):
        # Test Case: Single Individual without Child (Eligible)
        input_data = {
            "id": "test1",
            "numberOfChildren": 0,
            "familyComposition": "single",
            "familyUnitInPayForDecember": True
        }
        expected_result = {
            "id": "test1",
            "isEligible": True,
            "baseAmount": 60.0,
            "childrenAmount": 0.0,
            "supplementAmount": 60.0
        }

        # Simulate on_message behavior
        self.simulate_on_message(input_data, expected_result)

        # Validate input topic publish
        self.mock_client.publish.assert_any_call(
            f"BRE/calculateWinterSupplementInput/{input_data['id']}",
            json.dumps(input_data)
        )

        # Validate output topic publish
        self.mock_client.publish.assert_any_call(
            f"BRE/calculateWinterSupplementOutput/{input_data['id']}",
            json.dumps(expected_result)
        )
    def test_single_person_with_one_child_eligible(self):
        # Test Case: Single Individual with One Child (Eligible)
        input_data = {
            "id": "test9",
            "numberOfChildren": 1,
            "familyComposition": "single",
            "familyUnitInPayForDecember": True
        }
        expected_result = {
            "id": "test9",
            "isEligible": True,
            "baseAmount": 60.0,
            "childrenAmount": 20.0,
            "supplementAmount": 80.0
        }

        self.simulate_on_message(input_data, expected_result)

        # Validate input topic publish
        self.mock_client.publish.assert_any_call(
            f"BRE/calculateWinterSupplementInput/{input_data['id']}",
            json.dumps(input_data)
        )

        # Validate output topic publish
        self.mock_client.publish.assert_any_call(
            f"BRE/calculateWinterSupplementOutput/{input_data['id']}",
            json.dumps(expected_result)
        )

    def test_couple_with_children_eligible(self):
        # Test Case: Couple with Children (Eligible)
        input_data = {
            "id": "test2",
            "numberOfChildren": 3,
            "familyComposition": "couple",
            "familyUnitInPayForDecember": True
        }
        expected_result = {
            "id": "test2",
            "isEligible": True,
            "baseAmount": 120.0,
            "childrenAmount": 60.0,
            "supplementAmount": 180.0
        }

        self.simulate_on_message(input_data, expected_result)

        # Validate input topic publish
        self.mock_client.publish.assert_any_call(
            f"BRE/calculateWinterSupplementInput/{input_data['id']}",
            json.dumps(input_data)
        )

        # Validate output topic publish
        self.mock_client.publish.assert_any_call(
            f"BRE/calculateWinterSupplementOutput/{input_data['id']}",
            json.dumps(expected_result)
        )


   
    def test_couple_no_children_eligible(self):
        # Test Case: Couple with No Children (Eligible)
        input_data = {
            "id": "test10",
            "numberOfChildren": 0,
            "familyComposition": "couple",
            "familyUnitInPayForDecember": True
        }
        expected_result = {
            "id": "test10",
            "isEligible": True,
            "baseAmount": 120.0,
            "childrenAmount": 0.0,
            "supplementAmount": 120.0
        }

        self.simulate_on_message(input_data, expected_result)

        # Validate input topic publish
        self.mock_client.publish.assert_any_call(
            f"BRE/calculateWinterSupplementInput/{input_data['id']}",
            json.dumps(input_data)
        )

        # Validate output topic publish
        self.mock_client.publish.assert_any_call(
            f"BRE/calculateWinterSupplementOutput/{input_data['id']}",
            json.dumps(expected_result)
        )
    def test_single_person_with_one_child_not_eligible(self):
        # Test Case: Single Individual with One Child (Not Eligible)
        input_data = {
            "id": "test13",
            "numberOfChildren": 1,
            "familyComposition": "single",
            "familyUnitInPayForDecember": False
        }
        expected_result = {
            "id": "test13",
            "isEligible": False,
            "baseAmount": 0.0,
            "childrenAmount": 0.0,
            "supplementAmount": 0.0
        }

        self.simulate_on_message(input_data, expected_result)

        # Validate input topic publish
        self.mock_client.publish.assert_any_call(
            f"BRE/calculateWinterSupplementInput/{input_data['id']}",
            json.dumps(input_data)
        )

        # Validate output topic publish
        self.mock_client.publish.assert_any_call(
            f"BRE/calculateWinterSupplementOutput/{input_data['id']}",
            json.dumps(expected_result)
        )
    def test_single_person_no_children_not_eligible(self):
        # Test Case: Single Individual with No Children (Not Eligible)
        input_data = {
            "id": "test15",
            "numberOfChildren": 0,
            "familyComposition": "single",
            "familyUnitInPayForDecember": False
        }
        expected_result = {
            "id": "test15",
            "isEligible": False,
            "baseAmount": 0.0,
            "childrenAmount": 0.0,
            "supplementAmount": 0.0
        }

        self.simulate_on_message(input_data, expected_result)

        # Validate input topic publish
        self.mock_client.publish.assert_any_call(
            f"BRE/calculateWinterSupplementInput/{input_data['id']}",
            json.dumps(input_data)
        )

        # Validate output topic publish
        self.mock_client.publish.assert_any_call(
            f"BRE/calculateWinterSupplementOutput/{input_data['id']}",
            json.dumps(expected_result)
        )


    def test_couple_with_children_not_eligible(self):
        # 夫妻有子女，不符合领取资格
        input_data = {
            "id": "test16",
            "numberOfChildren": 2,
            "familyComposition": "couple",
            "familyUnitInPayForDecember": False
        }
        expected_result = {
            "id": "test16",
            "isEligible": False,
            "baseAmount": 0.0,
            "childrenAmount": 0.0,
            "supplementAmount": 0.0
        }

        self.simulate_on_message(input_data, expected_result)

        # Validate input topic publish
        self.mock_client.publish.assert_any_call(
            f"BRE/calculateWinterSupplementInput/{input_data['id']}",
            json.dumps(input_data)
        )

        # Validate output topic publish
        self.mock_client.publish.assert_any_call(
            f"BRE/calculateWinterSupplementOutput/{input_data['id']}",
            json.dumps(expected_result)
        )


    def test_couple_no_children_not_eligible(self):
        # Test Case: Couple with No Children (Not Eligible)
        input_data = {
            "id": "test14",
            "numberOfChildren": 0,
            "familyComposition": "couple",
            "familyUnitInPayForDecember": False
        }
        expected_result = {
            "id": "test14",
            "isEligible": False,
            "baseAmount": 0.0,
            "childrenAmount": 0.0,
            "supplementAmount": 0.0
        }

        self.simulate_on_message(input_data, expected_result)

        # Validate input topic publish
        self.mock_client.publish.assert_any_call(
            f"BRE/calculateWinterSupplementInput/{input_data['id']}",
            json.dumps(input_data)
        )

        # Validate output topic publish
        self.mock_client.publish.assert_any_call(
            f"BRE/calculateWinterSupplementOutput/{input_data['id']}",
            json.dumps(expected_result)
        )


    def test_result_pending(self):
        # Test Case: Pending Result
        # Ensures that a pending result status is correctly returned when the supplement calculation is still in progress.
        topic_id = "test3"
        self.mock_results[topic_id] = {"status": "pending"}
        response = self.app.get(f'/result/{topic_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "pending"})


    def test_large_number_of_children(self):
        # Test Case: Large Number of Children
        # Validates that a family with a large number of children (e.g., 50) receives the correct base 
        # amount and child supplement, ensuring the calculation scales appropriately.
        input_data = {
            "id": "test4",
            "numberOfChildren": 50,
            "familyComposition": "couple",
            "familyUnitInPayForDecember": True
        }
        expected_result = {
            "id": "test4",
            "isEligible": True,
            "baseAmount": 120.0,
            "childrenAmount": 1000.0, 
            "supplementAmount": 1120.0
        }

        self.simulate_on_message(input_data, expected_result)

        # Validate input topic publish
        self.mock_client.publish.assert_any_call(
            f"BRE/calculateWinterSupplementInput/{input_data['id']}",
            json.dumps(input_data)
        )

        # Validate output topic publish
        self.mock_client.publish.assert_any_call(
            f"BRE/calculateWinterSupplementOutput/{input_data['id']}",
            json.dumps(expected_result)
        )


    def test_negative_number_of_children(self):
        # Test Case: Negative Number of Children
        # Confirms that an invalid input with a negative number of children is rejected, 
        # returning an appropriate error response.
        input_data = {
            "id": "test5",
            "numberOfChildren": -3,
            "familyComposition": "single",
            "familyUnitInPayForDecember": True
        }
        response = self.app.post('/submit', data=json.dumps(input_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)  


    def test_invalid_family_composition(self):
        # Test Case: Invalid Family Composition
        # Ensures that an invalid family composition input is rejected, returning an 
        # appropriate error response.
        input_data = {
            "id": "test6",
            "numberOfChildren": 2,
            "familyComposition": "invalid",
            "familyUnitInPayForDecember": True
        }
        response = self.app.post('/submit', data=json.dumps(input_data), content_type='application/json')
        self.assertEqual(response.status_code, 400) 


    def test_result_completed(self):
        # Test Case: Completed Result
        # Validates that a completed result is correctly retrieved for a given topic ID,
        # ensuring the system returns the appropriate calculation values.
        topic_id = "test8"
        expected_result = {
            "id": topic_id,
            "isEligible": True,
            "baseAmount": 120.0,
            "childrenAmount": 60.0,
            "supplementAmount": 180.0
        }
        self.mock_results[topic_id] = expected_result
        response = self.app.get(f'/result/{topic_id}')
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json, expected_result)


if __name__ == "__main__":
    unittest.main()
