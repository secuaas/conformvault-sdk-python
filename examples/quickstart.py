"""Quickstart example for the ConformVault Python SDK.

Set the CONFORMVAULT_API_KEY environment variable before running::

    export CONFORMVAULT_API_KEY="cvk_live_your_api_key"
    python examples/quickstart.py
"""

from __future__ import annotations

import os
import sys

import conformvault
from conformvault import (
    ConformVault,
    CreateSignatureRequest,
    CreateSignatureSigner,
    is_rate_limited,
)


def main() -> None:
    api_key = os.environ.get("CONFORMVAULT_API_KEY", "")
    if not api_key:
        print("Error: CONFORMVAULT_API_KEY environment variable is required")
        sys.exit(1)

    # Create client (defaults to production URL)
    client = ConformVault(api_key)

    # List files
    files = client.files.list()
    print(f"Found {len(files)} files")
    for f in files:
        print(f"  - {f.original_name} ({f.id}, {f.size} bytes)")

    # List folders
    folders = client.folders.list()
    print(f"Found {len(folders)} folders")

    # Create a signature envelope (requires a file ID)
    if files:
        try:
            env = client.signatures.create(CreateSignatureRequest(
                file_id=files[0].id,
                subject="Please sign this document",
                signers=[
                    CreateSignatureSigner(
                        email="signer@example.com",
                        name="Jane Doe",
                        role="signer",
                    ),
                ],
                expiry_days=30,
            ))
            print(f"Signature envelope created: {env.id} (status: {env.status})")
        except Exception as e:
            if is_rate_limited(e):
                print("Rate limited! Try again later.")
            else:
                raise

    client.close()


if __name__ == "__main__":
    main()
