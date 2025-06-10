#!/usr/bin/env python3
"""
Test for creating a domain verification request.

This test demonstrates how to create a domain verification request
using the Freestyle SDK. The verification request returns a code
that needs to be added as a TXT record to complete domain verification.
"""

import freestyle
import os


# Initialize the client
client = freestyle.Freestyle(os.environ.get("FREESTYLE_API_KEY"))

# Domain to verify (use a test domain)
test_domain = "test-verification.example.com"


verification_request = client.create_domain_verification_request(
    domain=test_domain,
)

print("Domain verification request created successfully!")
print(f"Domain: {verification_request.domain}")
print(f"Verification Code: {verification_request.verification_code}")
print(f"Id: {verification_request.id}")
