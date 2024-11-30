import unittest
from rules_engine import calculate_winter_supplement

class TestRulesEngine(unittest.TestCase):

    def test_eligible_single_no_children(self):
        """Test: Single person, no children, eligible."""
        data = {
            "id": "test1",
            "familyComposition": "single",
            "numberOfChildren": 0,
            "familyUnitInPayForDecember": True,
        }
        result = calculate_winter_supplement(data)
        self.assertTrue(result["isEligible"])
        self.assertEqual(result["baseAmount"], 60)
        self.assertEqual(result["childrenAmount"], 0)
        self.assertEqual(result["supplementAmount"], 60)

    def test_eligible_couple_with_children(self):
        """Test: Couple with 2 children, eligible."""
        data = {
            "id": "test2",
            "familyComposition": "couple",
            "numberOfChildren": 2,
            "familyUnitInPayForDecember": True,
        }
        result = calculate_winter_supplement(data)
        self.assertTrue(result["isEligible"])
        self.assertEqual(result["baseAmount"], 120)
        self.assertEqual(result["childrenAmount"], 40)
        self.assertEqual(result["supplementAmount"], 160)

    def test_ineligible_single_no_children(self):
        """Test: Single person, no children, not eligible."""
        data = {
            "id": "test3",
            "familyComposition": "single",
            "numberOfChildren": 0,
            "familyUnitInPayForDecember": False,
        }
        result = calculate_winter_supplement(data)
        self.assertFalse(result["isEligible"])
        self.assertEqual(result["baseAmount"], 0)
        self.assertEqual(result["childrenAmount"], 0)
        self.assertEqual(result["supplementAmount"], 0)

    def test_eligible_single_with_children(self):
        """Test: Single person with 1 child, eligible."""
        data = {
            "id": "test4",
            "familyComposition": "single",
            "numberOfChildren": 1,
            "familyUnitInPayForDecember": True,
        }
        result = calculate_winter_supplement(data)
        self.assertTrue(result["isEligible"])
        self.assertEqual(result["baseAmount"], 60)
        self.assertEqual(result["childrenAmount"], 20)
        self.assertEqual(result["supplementAmount"], 80)

    def test_edge_case_no_children(self):
        """Edge Case: No children, valid inputs."""
        data = {
            "id": "test5",
            "familyComposition": "couple",
            "numberOfChildren": 0,
            "familyUnitInPayForDecember": True,
        }
        result = calculate_winter_supplement(data)
        self.assertTrue(result["isEligible"])
        self.assertEqual(result["baseAmount"], 120)
        self.assertEqual(result["childrenAmount"], 0)
        self.assertEqual(result["supplementAmount"], 120)

    def test_edge_case_max_children(self):
        """Edge Case: High number of children."""
        data = {
            "id": "test6",
            "familyComposition": "single",
            "numberOfChildren": 10,
            "familyUnitInPayForDecember": True,
        }
        result = calculate_winter_supplement(data)
        self.assertTrue(result["isEligible"])
        self.assertEqual(result["baseAmount"], 60)
        self.assertEqual(result["childrenAmount"], 200)
        self.assertEqual(result["supplementAmount"], 260)

    def test_invalid_family_composition(self):
        """Edge Case: Invalid family composition."""
        data = {
            "id": "test7",
            "familyComposition": "invalid",
            "numberOfChildren": 2,
            "familyUnitInPayForDecember": True,
        }
        result = calculate_winter_supplement(data)
        self.assertIsNone(result)

    def test_missing_field(self):
        """Edge Case: Missing required field."""
        data = {
            "id": "test8",
            "familyComposition": "single",
            "numberOfChildren": 1,
            # Missing 'familyUnitInPayForDecember'
        }
        with self.assertRaises(KeyError):
            calculate_winter_supplement(data)

    def test_negative_children(self):
        """Edge Case: Negative number of children."""
        data = {
            "id": "test9",
            "familyComposition": "couple",
            "numberOfChildren": -1,
            "familyUnitInPayForDecember": True,
        }
        result = calculate_winter_supplement(data)
        self.assertIsNone(result)

    def test_zero_children(self):
        """Test: Zero children for both single and couple."""
        data_single = {
            "id": "test10",
            "familyComposition": "single",
            "numberOfChildren": 0,
            "familyUnitInPayForDecember": True,
        }
        result_single = calculate_winter_supplement(data_single)
        self.assertTrue(result_single["isEligible"])
        self.assertEqual(result_single["baseAmount"], 60)
        self.assertEqual(result_single["childrenAmount"], 0)
        self.assertEqual(result_single["supplementAmount"], 60)

        data_couple = {
            "id": "test11",
            "familyComposition": "couple",
            "numberOfChildren": 0,
            "familyUnitInPayForDecember": True,
        }
        result_couple = calculate_winter_supplement(data_couple)
        self.assertTrue(result_couple["isEligible"])
        self.assertEqual(result_couple["baseAmount"], 120)
        self.assertEqual(result_couple["childrenAmount"], 0)
        self.assertEqual(result_couple["supplementAmount"], 120)

if __name__ == "__main__":
    unittest.main()
