import re

class OrderExtractor:
    @staticmethod
    def extract_order_id(raw_text: str):
        reasons = []
        # Match 'ORD-100001' style Order IDs
        match = re.search(r'(ORD-\d+)', raw_text, re.IGNORECASE)
        if match:
            reasons.append("Matched ORD format regex")
            return match.group(1), reasons
            
        return "UNKNOWN_ORDER", ["Order ID not found"]
