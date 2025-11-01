#!/usr/bin/env python3
"""
Performance comparison between original and optimized email validation functions.
"""

import time
import re
from typing import List


def original_is_valid_email(email):
    """Original implementation with multiple string operations"""
    if "@" not in email or "." not in email:
        return False
    local_part, domain = email.split("@", 1)
    if not local_part or not domain or "." not in domain:
        return False
    if domain.startswith(".") or domain.endswith("."):
        return False
    if ".." in domain:
        return False
    return True


def optimized_is_valid_email(email):
    """
    Optimized email validation function.
    Reduces redundant string operations while maintaining original logic.
    """
    # Combined early checks to reduce function calls
    if not email or "@" not in email:
        return False
    
    # Single split operation instead of multiple checks
    parts = email.split("@", 1)
    if len(parts) != 2:
        return False
    
    local_part, domain = parts
    
    # Combined checks using short-circuit evaluation
    if (not local_part or 
        not domain or 
        "." not in domain or
        domain.startswith(".") or 
        domain.endswith(".") or
        ".." in domain):
        return False
    
    return True


def benchmark_function(func, test_emails: List[str], iterations: int = 1000) -> float:
    """Benchmark a function with given test emails"""
    start_time = time.perf_counter()
    
    for _ in range(iterations):
        for email in test_emails:
            func(email)
    
    end_time = time.perf_counter()
    return end_time - start_time


def main():
    # Test emails (mix of valid and invalid)
    test_emails = [
        "user@example.com",
        "test.email@domain.org",
        "invalid.email",
        "user@domain..com",
        "user123@test-domain.co.uk",
        "@invalid.com",
        "first.last@subdomain.example.com",
        "user+tag@example.com",
        "plainaddress",
        "missing@domain.",
    ]
    
    iterations = 10000
    
    print("Email Validation Performance Comparison")
    print("=" * 50)
    print(f"Test emails: {len(test_emails)}")
    print(f"Iterations: {iterations}")
    print(f"Total function calls: {len(test_emails) * iterations:,}")
    print()
    
    # Benchmark original function
    original_time = benchmark_function(original_is_valid_email, test_emails, iterations)
    print(f"Original implementation: {original_time:.4f} seconds")
    
    # Benchmark optimized function
    optimized_time = benchmark_function(optimized_is_valid_email, test_emails, iterations)
    print(f"Optimized implementation: {optimized_time:.4f} seconds")
    
    # Calculate improvement
    if original_time > 0:
        speedup = original_time / optimized_time
        improvement = ((original_time - optimized_time) / original_time) * 100
        
        print()
        print("Results:")
        print(f"Speedup: {speedup:.2f}x")
        print(f"Performance improvement: {improvement:.1f}%")
        
        if speedup > 1:
            print(f"✅ Optimized version is {speedup:.2f}x faster!")
        else:
            print(f"⚠️  Original version was {1/speedup:.2f}x faster")
    
    # Verify both functions produce the same results
    print("\nVerifying correctness...")
    all_match = True
    for email in test_emails:
        original_result = original_is_valid_email(email)
        optimized_result = optimized_is_valid_email(email)
        
        if original_result != optimized_result:
            print(f"❌ Mismatch for '{email}': original={original_result}, optimized={optimized_result}")
            all_match = False
    
    if all_match:
        print("✅ All results match - optimization is correct!")
    else:
        print("❌ Some results don't match - check implementation!")


if __name__ == "__main__":
    main()