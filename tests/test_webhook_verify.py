"""Tests for webhook signature verification."""

from __future__ import annotations

import hashlib
import hmac
import time

from conformvault import verify_webhook_signature


class TestWebhookVerify:

    def test_valid_raw_hmac(self):
        """Go SDK compatibility: raw HMAC hex digest."""
        secret = "whsec_test123"
        payload = b'{"event":"file.uploaded","file_id":"f1"}'

        mac = hmac.new(secret.encode(), payload, hashlib.sha256)
        sig = mac.hexdigest()

        assert verify_webhook_signature(payload, sig, secret) is True

    def test_invalid_raw_hmac(self):
        payload = b'{"event":"file.uploaded"}'
        assert verify_webhook_signature(payload, "bad_signature", "whsec_test123") is False

    def test_wrong_secret_raw(self):
        secret = "whsec_test123"
        payload = b'{"event":"file.uploaded"}'

        mac = hmac.new(secret.encode(), payload, hashlib.sha256)
        sig = mac.hexdigest()

        assert verify_webhook_signature(payload, sig, "wrong-secret") is False

    def test_valid_structured_header(self):
        """Structured header format: t=<timestamp>,s0=<hmac>."""
        secret = "whsec_structured"
        payload = b'{"event":"file.deleted","file_id":"f2"}'
        timestamp = str(int(time.time()))

        signed_content = f"{timestamp}.".encode() + payload
        mac = hmac.new(secret.encode(), signed_content, hashlib.sha256)
        sig = mac.hexdigest()

        header = f"t={timestamp},s0={sig}"
        assert verify_webhook_signature(payload, header, secret) is True

    def test_invalid_structured_header(self):
        secret = "whsec_structured"
        payload = b'{"event":"file.deleted"}'
        header = "t=1234567890,s0=deadbeef"
        assert verify_webhook_signature(payload, header, secret) is False

    def test_wrong_timestamp_structured(self):
        """A different timestamp produces a different HMAC."""
        secret = "whsec_ts"
        payload = b'{"event":"test"}'
        ts1 = "1000000000"
        ts2 = "2000000000"

        signed = f"{ts1}.".encode() + payload
        mac = hmac.new(secret.encode(), signed, hashlib.sha256)
        sig = mac.hexdigest()

        # Verify with correct timestamp
        assert verify_webhook_signature(payload, f"t={ts1},s0={sig}", secret) is True
        # Wrong timestamp should fail
        assert verify_webhook_signature(payload, f"t={ts2},s0={sig}", secret) is False

    def test_string_payload(self):
        """Payload can be passed as str instead of bytes."""
        secret = "whsec_str"
        payload_str = '{"event":"file.uploaded"}'
        payload_bytes = payload_str.encode()

        mac = hmac.new(secret.encode(), payload_bytes, hashlib.sha256)
        sig = mac.hexdigest()

        assert verify_webhook_signature(payload_str, sig, secret) is True

    def test_empty_structured_fields(self):
        """Structured header with missing fields should fail gracefully."""
        assert verify_webhook_signature(b"data", "t=,s0=", "secret") is False
        assert verify_webhook_signature(b"data", "t=123,s0=", "secret") is False
        assert verify_webhook_signature(b"data", "t=,s0=abc", "secret") is False
