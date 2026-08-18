import re

class OrderExtractor:
    @staticmethod
    def extract_order_id(raw_text: str):
        reasons = []
        # Match 'ORD-100001', 'Order ID: 12345', 'Order # 12345'
        patterns = [
            r'(ORD-\d+)',
            r'Order\s*ID\s*[:\-]?\s*([A-Za-z0-9\-]+)',
            r'Order\s*#?\s*[:\-]?\s*([A-Za-z0-9\-]+)'
        ]
        for pattern in patterns:
            match = re.search(pattern, raw_text, re.IGNORECASE)
            if match:
                reasons.append(f"Matched order format")
                return match.group(1), reasons
                
        return "UNKNOWN_ORDER", ["Order ID not found"]
