GST_STATE_CODES = {
    "01": ("Jammu and Kashmir", False),
    "02": ("Himachal Pradesh", False),
    "03": ("Punjab", False),
    "04": ("Chandigarh", True),
    "05": ("Uttarakhand", False),
    "06": ("Haryana", False),
    "07": ("Delhi", True),
    "08": ("Rajasthan", False),
    "09": ("Uttar Pradesh", False),
    "10": ("Bihar", False),
    "11": ("Sikkim", False),
    "12": ("Arunachal Pradesh", False),
    "13": ("Nagaland", False),
    "14": ("Manipur", False),
    "15": ("Mizoram", False),
    "16": ("Tripura", False),
    "17": ("Meghalaya", False),
    "18": ("Assam", False),
    "19": ("West Bengal", False),
    "20": ("Jharkhand", False),
    "21": ("Odisha", False),
    "22": ("Chhattisgarh", False),
    "23": ("Madhya Pradesh", False),
    "24": ("Gujarat", False),
    "25": ("Daman and Diu", True),
    "26": ("Dadra and Nagar Haveli and Daman and Diu", True),
    "27": ("Maharashtra", False),
    "29": ("Karnataka", False),
    "30": ("Goa", False),
    "31": ("Lakshadweep", True),
    "32": ("Kerala", False),
    "33": ("Tamil Nadu", False),
    "34": ("Puducherry", True),
    "35": ("Andaman and Nicobar Islands", True),
    "36": ("Telangana", False),
    "37": ("Andhra Pradesh", False),
    "38": ("Ladakh", True),
    "97": ("Other Territory", True),
    "99": ("Centre Jurisdiction", True),
}

class GSTStateMaster:
    @staticmethod
    def get_state(code: str) -> dict | None:
        state_data = GST_STATE_CODES.get(code)
        if not state_data:
            return None
        return {
            "code": code,
            "name": state_data[0],
            "is_union_territory": state_data[1]
        }

    @staticmethod
    def get_state_name(code: str) -> str | None:
        state_data = GST_STATE_CODES.get(code)
        return state_data[0] if state_data else None

    @staticmethod
    def is_valid_state_code(code: str) -> bool:
        return code in GST_STATE_CODES

    @staticmethod
    def all_states() -> list[dict]:
        return [
            {
                "code": code,
                "name": data[0],
                "is_union_territory": data[1]
            }
            for code, data in sorted(GST_STATE_CODES.items())
        ]

    @staticmethod
    def get_by_name(name: str) -> dict | None:
        name_lower = name.lower()
        for code, data in GST_STATE_CODES.items():
            if data[0].lower() == name_lower:
                return {
                    "code": code,
                    "name": data[0],
                    "is_union_territory": data[1]
                }
        return None
