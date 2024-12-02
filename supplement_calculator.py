"""
Winter Supplement Calculator
Author: Liliya
----------------------------
This module calculates winter supplement amounts based on family type, number of children, 
and eligibility criteria. 

Key Rules:
1. Single, childless individuals get $60 per year.
2. Childless couples get $120 per year.
3. Families with children get $120 base plus $20 per child.

Main Functions:
- calculate_base_amount: Determines the base amount.
- calculate_children_amount: Calculates the child supplement.
- calculate_supplement: Computes the total amount.
"""

# Business Logic Constants
BASE_AMOUNT_SINGLE_NO_CHILDREN = 60.0  # Single person with no children
BASE_AMOUNT_COUPLE_NO_CHILDREN = 120.0  # Childless couple
BASE_AMOUNT_WITH_CHILDREN = 120.0  # Base amount for families with dependent children
CHILD_SUPPLEMENT = 20.0  # Supplement amount per dependent child

def calculate_base_amount(family_composition, number_of_children):
    """
    Calculate the base amount based on family composition and number of children.

    :param family_composition: str
        The family composition, either "single" or "couple".
    :param number_of_children: int
        The number of dependent children.
    :return: float
        The base amount calculated based on the family composition and number of children.
    :raises ValueError:
        If the family composition is invalid.
    """
    if number_of_children == 0:
        if family_composition == "single":
            return BASE_AMOUNT_SINGLE_NO_CHILDREN
        elif family_composition == "couple":
            return BASE_AMOUNT_COUPLE_NO_CHILDREN
        else:
            raise ValueError("Invalid family composition")
    else:
        return BASE_AMOUNT_WITH_CHILDREN

def calculate_children_amount(number_of_children):
    """
    Calculate the supplement amount based on the number of children.

    :param number_of_children: int
        The number of dependent children.
    :return: float
        The supplement amount calculated based on the number of dependent children.
    """
    return number_of_children * CHILD_SUPPLEMENT

def calculate_supplement(data):
    """
    Calculate the total supplement based on input data.

    :param data: dict
        Input data containing the following keys:
        - familyComposition (str): "single" or "couple".
        - numberOfChildren (int): Number of dependent children (default is 0).
        - familyUnitInPayForDecember (bool): Whether the family unit is eligible for payment in December.
    :return: dict
        A dictionary containing:
        - isEligible (bool): Whether the family is eligible for the supplement.
        - baseAmount (float): The base amount calculated.
        - childrenAmount (float): The supplement amount for dependent children.
        - supplementAmount (float): The total supplement amount (base + children).
    """
    if data.get("familyUnitInPayForDecember"):
        number_of_children = data.get("numberOfChildren", 0)
        family_composition = data.get("familyComposition")

        base_amount = calculate_base_amount(family_composition, number_of_children)
        children_amount = calculate_children_amount(number_of_children) if number_of_children > 0 else 0.0
        total_amount = base_amount + children_amount

        return {
            "isEligible": True,
            "baseAmount": base_amount,
            "childrenAmount": children_amount,
            "supplementAmount": total_amount,
        }
    else:
        return {
            "isEligible": False,
            "baseAmount": 0.0,
            "childrenAmount": 0.0,
            "supplementAmount": 0.0,
        }
