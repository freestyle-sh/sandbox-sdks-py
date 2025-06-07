import os
import sys

import freestyle

# Get API token from environment variable
token = os.getenv("FREESTYLE_API_KEY")
if not token:
    print("Please set FREESTYLE_API_KEY environment variable")
    sys.exit(1)

# Initialize the client
client = freestyle.Freestyle(token=token)

# Example domain to verify (replace with your own domain)
domain = "example.com"

try:
    print(f"Creating domain verification request for: {domain}")

    # Step 1: Create domain verification request
    verification_response = client.create_domain_verification_request(domain)
    print(f"✅ Domain verification request created!")
    print(f"Verification code: {verification_response.verification_code}")
    print(f"Verification ID: {verification_response.id}")

    print(f"\n📋 Next steps:")
    print(f"1. Add a TXT record to your DNS:")
    print(f"   Name: _freestyle_custom_hostname.{domain}")
    print(f"   Value: {verification_response.verification_code}")
    print(f"2. Wait for DNS propagation (usually 5-15 minutes)")
    print(f"3. Run the verification step below")

    # Step 2: List current verification requests
    print(f"\n📄 Current domain verification requests:")
    verification_requests = client.list_domain_verification_requests()
    for req in verification_requests:
        print(
            f"  - Domain: {req.domain}, Code: {req.verification_code}, Created: {req.created_at}"
        )

    # Step 3: Verify domain (uncomment when DNS is set up)
    print(
        f"\n⚠️  To complete verification, uncomment the lines below and run again after setting up DNS:"
    )
    print(f"# verify_result = client.verify_domain('{domain}')")
    print(f"# print(f'Domain verification result: {{verify_result}}')")

    # verify_result = client.verify_domain(domain)
    # print(f"Domain verification result: {verify_result}")

    # Step 4: List verified domains
    print(f"\n📋 Currently verified domains:")
    domains = client.list_domains()
    for domain_info in domains:
        print(f"  - {domain_info.domain}")

    # Step 5: Example of provisioning wildcard (uncomment after verification)
    print(
        f"\n⚠️  To provision wildcard certificate, uncomment after domain is verified:"
    )
    print(f"# wildcard_result = client.provision_wildcard('{domain}')")
    print(f"# print(f'Wildcard provisioning result: {{wildcard_result}}')")

    # wildcard_result = client.provision_wildcard(domain)
    # print(f"Wildcard provisioning result: {wildcard_result}")

except Exception as e:
    print(f"❌ Error: {e}")

    # If there's an error, show how to clean up
    print(f"\n🧹 To clean up verification request:")
    print(
        f"# client.delete_domain_verification_request('{domain}', 'verification_code_here')"
    )
