import re
from backend.utils.logger import logger

class CustomerExtractor:
    @staticmethod
    def extract_customer_name(text: str) -> tuple[str, list[str]]:
        """Extracts customer name from the raw text using patterns."""
        reasons = []
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        for i, line in enumerate(lines):
            # If Customer Address is found, the name is usually the next line or on the same line
            if "Customer Address" in line or "Ship To:" in line or "Customer Name:" in line:
                reasons.append("Found customer keyword")
                
                # Check if name is on the same line (e.g. 'Ship To: Rahul')
                match = re.search(r"(?:Ship To:|Customer Name:|Consignee:|Customer Address:?)\s+([A-Za-z\s]+)", line, re.IGNORECASE)
                if match:
                    name_part = match.group(1).strip()
                    # Filter out grid text like 'Valmo'
                    if name_part and not name_part.lower().startswith('valmo'):
                        return name_part, reasons
                
                # Otherwise, it's on the next line (e.g. Meesho format)
                if i + 1 < len(lines):
                    next_line = lines[i+1]
                    # Clean up grid artifact on next line (e.g. 'shreya pandey FSC-R0')
                    name = re.split(r'\s{2,}|FSC|Valmo', next_line)[0].strip()
                    return name, reasons

        return "Unknown Customer", reasons

    @staticmethod
    def extract_customer_address(text: str) -> tuple[str, list[str]]:
        """Extracts shipping/customer address from raw text."""
        reasons = []
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        for i, line in enumerate(lines):
            if "Customer Address" in line or "Ship To:" in line:
                reasons.append("Address keyword detected")
                
                address_lines = []
                # Grab the next few lines as address (skipping the name line)
                for j in range(i + 2, min(i + 5, len(lines))):
                    addr_line = lines[j]
                    if "If undelivered" in addr_line or "Product Details" in addr_line:
                        break
                    # Clean up grid artifacts on the right
                    clean_addr = re.split(r'\s{2,}|N1/|N2/|B-4|Valmo|FSC', addr_line)[0].strip()
                    if clean_addr:
                        address_lines.append(clean_addr)
                        
                if address_lines:
                    return ", ".join(address_lines), reasons
                
        reasons.append("Defaulting address block")
        return "Address not specified", reasons