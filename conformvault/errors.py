"""Exception hierarchy for the ConformVault Python SDK."""

from __future__ import annotations


class ConformVaultError(Exception):
    """Base exception for all ConformVault SDK errors."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class APIError(ConformVaultError):
    """Error returned by the ConformVault API (HTTP 4xx/5xx)."""

    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        super().__init__(message)

    def __str__(self) -> str:
        return f"conformvault: HTTP {self.status_code}: {self.message}"

    def __repr__(self) -> str:
        return f"APIError(status_code={self.status_code}, message={self.message!r})"


class AuthenticationError(APIError):
    """Raised when the API returns 401 Unauthorized or 403 Forbidden."""

    def __init__(self, message: str = "authentication failed") -> None:
        super().__init__(status_code=401, message=message)


class RateLimitError(APIError):
    """Raised when the API returns 429 Too Many Requests."""

    def __init__(self, retry_after: float = 60.0, message: str = "rate limited") -> None:
        self.retry_after = retry_after
        super().__init__(status_code=429, message=message)

    def __str__(self) -> str:
        return f"conformvault: rate limited (retry after {self.retry_after}s)"

    def __repr__(self) -> str:
        return f"RateLimitError(retry_after={self.retry_after})"


def is_not_found(error: Exception) -> bool:
    """Return True if the error is a 404 Not Found."""
    return isinstance(error, APIError) and error.status_code == 404


def is_rate_limited(error: Exception) -> bool:
    """Return True if the error is a 429 Too Many Requests."""
    return isinstance(error, RateLimitError)
