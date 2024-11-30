def calculate_winter_supplement(data):
    try:
        # 检查必填字段
        required_fields = ["id", "familyComposition", "numberOfChildren", "familyUnitInPayForDecember"]
        for field in required_fields:
            if field not in data:
                raise KeyError(f"Missing required field: {field}")

        # 提取字段
        family_id = data["id"]
        family_composition = data["familyComposition"]
        number_of_children = data["numberOfChildren"]
        family_unit_in_pay_for_december = data["familyUnitInPayForDecember"]

        # 检查家庭构成是否有效
        if family_composition not in ["single", "couple"]:
            return None

        # 检查子女数量是否有效
        if number_of_children < 0:
            return None

        # 判断资格
        is_eligible = family_unit_in_pay_for_december
        base_amount = 0
        if is_eligible:
            base_amount = 60 if family_composition == "single" else 120
        children_amount = number_of_children * 20 if is_eligible else 0
        supplement_amount = base_amount + children_amount

        return {
            "id": family_id,
            "isEligible": is_eligible,
            "baseAmount": base_amount,
            "childrenAmount": children_amount,
            "supplementAmount": supplement_amount,
        }

    except KeyError as e:
        print(f"KeyError: {e}")
        raise
