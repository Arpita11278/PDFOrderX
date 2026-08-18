import re
from backend.utils.logger import logger

class CustomerExtractor:
    @staticmethod
    def extract_customer_name(text: str) -> tuple[str, list[str]]:
        """Extracts customer name from the raw text using patterns."""
        reasons = []
        # Common patterns for shipping/customer names
        patterns = [
            r"(?:Ship To:|Customer Name:|Consignee:)\s*([A-Za-z\s]+)",
            r"Buyer:\s*([A-Za-z\s]+)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                name = match.group(1).strip().split('\n')[0]
                reasons.append(f"Customer name found using pattern: {pattern}")
                return name, reasons
                
        reasons.append("Customer name not found via standard patterns, using fallback")
        return "Unknown Customer", reasons

    @staticmethod
    def extract_customer_address(text: str) -> tuple[str, list[str]]:
        """Extracts shipping/customer address from raw text."""
        reasons = []
        # Look for address block indicators
        if "Address:" in text or "Ship To:" in text:
            reasons.append("Address keyword detected")
            # Simple line-based fallback for extraction
            lines = text.split('\n')
            address_lines = []
            capture = False
            for line in lines:
                if "Ship To:" in line or "Address:" in line:
                    capture = True
                    continue
                if capture and line.strip() == "":
                    break
                if capture:
                    address_lines.append(line.strip())
            if address_lines:
                return ", ".join(address_lines), reasons
                
        reasons.append("Defaulting address block")
        return "Address not specified", reasons