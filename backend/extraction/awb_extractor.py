import re

class AWBExtractor:
    @staticmethod
    def extract_awb(raw_text: str):
        reasons = []
        # Match 'AWB700000137' style AWB numbers
        match = re.search(r'(AWB\d+)', raw_text, re.IGNORECASE)
        if match:
            reasons.append("Matched AWB format regex")
            return match.group(1), reasons
            
        return "UNKNOWN_AWB", ["AWB not found"]
