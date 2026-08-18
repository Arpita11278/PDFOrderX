import re

class AWBExtractor:
    @staticmethod
    def extract_awb(raw_text: str):
        reasons = []
        # Match 'AWB700000137', 'AWB Number: 12345', 'Tracking: 12345', 'Waybill: 12345'
        patterns = [
            r'(AWB\d+)',
            r'AWB\s*(?:Number|No)?\s*[:\-]?\s*([A-Za-z0-9\-]+)',
            r'(?:Tracking|Waybill)\s*(?:Number|No)?\s*[:\-]?\s*([A-Za-z0-9\-]+)'
        ]
        for pattern in patterns:
            match = re.search(pattern, raw_text, re.IGNORECASE)
            if match:
                reasons.append(f"Matched AWB format")
                return match.group(1), reasons
                
        return "UNKNOWN_AWB", ["AWB not found"]
