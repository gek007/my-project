import unittest
import time
from src.main import is_valid_email, is_email_from_domain

class TestEmailValidation(unittest.TestCase):

    def test_valid_emails(self):
        """Test valid email addresses"""
        valid_emails = [
            "user@example.com",
            "test.email@domain.org",
            "user123@test-domain.co.uk",
            "first.last@subdomain.example.com",
            "user+tag@example.com"
        ]
        
        for email in valid_emails:
            with self.subTest(email=email):
                self.assertTrue(is_valid_email(email), f"Expected {email} to be valid")

    def test_invalid_emails(self):
        """Test invalid email addresses (based on original function logic)"""
        invalid_emails = [
            "plainaddress",           # No @ symbol
            "@missinglocal.com",      # Missing local part
            "missing@.com",           # Domain starts with dot
            "missing@domain.",        # Domain ends with dot
            "user@domain..com",       # Double dot in domain
            "user@",                  # Missing domain
            "user@domain",            # Missing TLD
            "",                       # Empty string
        ]
        
        for email in invalid_emails:
            with self.subTest(email=email):
                self.assertFalse(is_valid_email(email), f"Expected {email} to be invalid")

    def test_edge_cases(self):
        """Test edge cases (based on original function behavior)"""
        edge_cases = [
            ("user@domain.c", True),     # Original function allows short TLD
            ("user@domain.toolong", True),  # Long but valid TLD
            ("a@b.co", True),             # Minimal valid email
            ("user..name@domain.com", True),  # Original allows double dots in local part
        ]
        
        for email, expected in edge_cases:
            with self.subTest(email=email):
                self.assertEqual(is_valid_email(email), expected)

class TestEmailFromDomain(unittest.TestCase):

    def test_valid_email_matching_domain(self):
        """Test valid emails from matching domains"""
        test_cases = [
            ("user@example.com", "example.com"),
            ("test.email@domain.org", "domain.org"),
            ("user123@test-domain.co.uk", "test-domain.co.uk"),
            ("first.last@subdomain.example.com", "subdomain.example.com"),
            ("user+tag@gmail.com", "gmail.com")
        ]
        
        for email, domain in test_cases:
            with self.subTest(email=email, domain=domain):
                self.assertTrue(is_email_from_domain(email, domain))

    def test_valid_email_non_matching_domain(self):
        """Test valid emails from non-matching domains"""
        test_cases = [
            ("user@example.com", "gmail.com"),
            ("test.email@domain.org", "example.com"),
            ("user123@test-domain.co.uk", "domain.org"),
            ("user@subdomain.example.com", "example.com"),  # subdomain vs main domain
            ("user@example.com", "example.org")  # different TLD
        ]
        
        for email, domain in test_cases:
            with self.subTest(email=email, domain=domain):
                self.assertFalse(is_email_from_domain(email, domain))

    def test_invalid_email_any_domain(self):
        """Test that invalid emails return False regardless of domain"""
        invalid_emails = [
            "plainaddress",
            "@missinglocal.com",
            "missing@.com",
            "user@",
            "",
            "user@domain"
        ]
        
        test_domain = "example.com"
        
        for email in invalid_emails:
            with self.subTest(email=email):
                self.assertFalse(is_email_from_domain(email, test_domain))

    def test_case_sensitivity(self):
        """Test case sensitivity in domain comparison"""
        test_cases = [
            ("user@Example.com", "example.com", False),  # Email domain uppercase
            ("user@example.com", "Example.com", False),  # Target domain uppercase
            ("user@EXAMPLE.COM", "example.com", False),  # Both different cases
            ("user@example.com", "example.com", True),   # Exact match
        ]
        
        for email, domain, expected in test_cases:
            with self.subTest(email=email, domain=domain):
                self.assertEqual(is_email_from_domain(email, domain), expected)

    def test_edge_cases(self):
        """Test edge cases and boundary conditions"""
        test_cases = [
            ("user@a.co", "a.co", True),              # Minimal domain
            ("user@domain.c", "domain.c", True),      # Short TLD
            ("user@sub.domain.com", "domain.com", False),  # Subdomain mismatch
            ("user@domain.com", "sub.domain.com", False),  # Main vs subdomain
        ]
        
        for email, domain, expected in test_cases:
            with self.subTest(email=email, domain=domain):
                self.assertEqual(is_email_from_domain(email, domain), expected)

    def test_empty_and_none_inputs(self):
        """Test empty strings and edge input cases"""
        # Empty domain parameter
        self.assertFalse(is_email_from_domain("user@example.com", ""))
        
        # Both empty
        self.assertFalse(is_email_from_domain("", ""))

if __name__ == '__main__':
    unittest.main()