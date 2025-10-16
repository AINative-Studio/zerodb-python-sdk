"""
Custom exceptions for ZeroDB MCP Client
"""

from typing import Optional, Dict, Any


class ZeroDBError(Exception):
    """Base exception for all ZeroDB client errors"""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.response_data = response_data or {}
        super().__init__(self.message)

    def __str__(self):
        if self.status_code:
            return f"[{self.status_code}] {self.message}"
        return self.message


class AuthenticationError(ZeroDBError):
    """Authentication failed - invalid API key or JWT token"""

    def __init__(self, message: str = "Authentication failed", **kwargs):
        super().__init__(message, status_code=401, **kwargs)


class RateLimitError(ZeroDBError):
    """Rate limit exceeded"""

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after: Optional[int] = None,
        **kwargs
    ):
        super().__init__(message, status_code=429, **kwargs)
        self.retry_after = retry_after

    def __str__(self):
        base = super().__str__()
        if self.retry_after:
            return f"{base} - Retry after {self.retry_after} seconds"
        return base


class ValidationError(ZeroDBError):
    """Request validation failed"""

    def __init__(self, message: str, errors: Optional[Dict] = None, **kwargs):
        super().__init__(message, status_code=422, **kwargs)
        self.errors = errors or {}

    def __str__(self):
        base = super().__str__()
        if self.errors:
            return f"{base}\nValidation errors: {self.errors}"
        return base


class ResourceNotFoundError(ZeroDBError):
    """Requested resource not found"""

    def __init__(self, resource_type: str, resource_id: str, **kwargs):
        message = f"{resource_type} '{resource_id}' not found"
        super().__init__(message, status_code=404, **kwargs)
        self.resource_type = resource_type
        self.resource_id = resource_id


class QuotaExceededError(ZeroDBError):
    """User quota exceeded"""

    def __init__(
        self,
        message: str = "Quota exceeded",
        quota_type: Optional[str] = None,
        current: Optional[int] = None,
        limit: Optional[int] = None,
        **kwargs
    ):
        super().__init__(message, status_code=402, **kwargs)
        self.quota_type = quota_type
        self.current = current
        self.limit = limit

    def __str__(self):
        base = super().__str__()
        if self.quota_type and self.current is not None and self.limit is not None:
            return f"{base} - {self.quota_type}: {self.current}/{self.limit}"
        return base


class NetworkError(ZeroDBError):
    """Network connectivity error"""

    def __init__(self, message: str = "Network error occurred", **kwargs):
        super().__init__(message, **kwargs)


class TimeoutError(ZeroDBError):
    """Request timeout"""

    def __init__(self, message: str = "Request timeout", timeout: Optional[float] = None, **kwargs):
        super().__init__(message, **kwargs)
        self.timeout = timeout

    def __str__(self):
        base = super().__str__()
        if self.timeout:
            return f"{base} after {self.timeout}s"
        return base


class ServerError(ZeroDBError):
    """Server error (5xx)"""

    def __init__(self, message: str = "Internal server error", **kwargs):
        super().__init__(message, status_code=500, **kwargs)


class ConflictError(ZeroDBError):
    """Resource conflict (e.g., duplicate resource)"""

    def __init__(self, message: str = "Resource conflict", **kwargs):
        super().__init__(message, status_code=409, **kwargs)
