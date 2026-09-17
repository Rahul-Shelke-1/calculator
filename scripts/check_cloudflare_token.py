from __future__ import annotations

import os
import sys

import requests

from dotenv import load_dotenv

load_dotenv()

API_BASE = "https://api.cloudflare.com/client/v4"


def main() -> int:
    token = os.getenv("CLOUDFLARE_API_TOKEN")
    account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")

    if not token:
        print("❌ CLOUDFLARE_API_TOKEN is not set.")
        return 1

    if not account_id:
        print("❌ CLOUDFLARE_ACCOUNT_ID is not set.")
        return 1

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    # 1. Verify token
    print("Checking Cloudflare API token...")

    # response = requests.get(
    #     f"{API_BASE}/user/tokens/verify",
    #     headers=headers,
    #     timeout=10,
    # )

    response = requests.get(
        f"{API_BASE}/accounts/{account_id}",
        headers=headers,
        timeout=10,
    )

    print("HTTP:", response.status_code)
    print(response.json())

    if response.status_code != 200:
        print(f"❌ Token verification failed: HTTP {response.status_code}")
        print(response.json())
        return 1

    result = response.json()

    if not result.get("success"):
        print("❌ Cloudflare rejected the token.")
        print(result)
        return 1

    token_status = result.get("result", {}).get("status")

    print(f"✅ Token is valid: {token_status}")

    # 2. Check account access
    print("Checking Cloudflare account access...")

    response = requests.get(
        f"{API_BASE}/accounts/{account_id}",
        headers=headers,
        timeout=10,
    )

    if response.status_code != 200:
        print(f"❌ Account access failed: HTTP {response.status_code}")
        print(response.json())
        return 1

    result = response.json()

    if not result.get("success"):
        print("❌ Token cannot access this Cloudflare account.")
        print(result)
        return 1

    account = result.get("result", {})

    print("✅ Cloudflare account access confirmed.")
    print(f"   Account: {account.get('name')}")
    print(f"   Account ID: {account.get('id')}")

    print("\n🎉 Cloudflare authentication is working.")

    return 0


if __name__ == "__main__":
    sys.exit(main())