import unittest
from backend.extraction.customer_extractor import CustomerExtractor

class TestCustomerExtractor(unittest.TestCase):
    def test_extract_customer_name(self):
        sample_text = "Ship To:\nJohn Doe\n123 Main Street\nCityville"
        name, reasons = CustomerExtractor.extract_customer_name(sample_text)
        self.assertEqual(name, "John Doe")
        self.assertTrue(len(reasons) > 0)

    def test_extract_customer_address(self):
        sample_text = "Ship To:\nJohn Doe\n123 Main Street\nCityville, State 12345\nOrder No: 98765"
        address, reasons = CustomerExtractor.extract_customer_address(sample_text)
        self.assertIn("123 Main Street", address)
        self.assertIn("Cityville, State 12345", address)

if __name__ == "__main__":
    unittest.main()