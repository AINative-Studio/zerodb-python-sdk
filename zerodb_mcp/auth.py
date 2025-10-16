"""
Authentication handler for ZeroDB MCP Client
"""

import os
from typing import Optional, Dict
from datetime import datetime, timedelta


class AuthHandler:
    """
    Handles authentication for ZeroDB MCP Bridge

    Supports:
    - API Key authentication (X-API-Key header)
    - JWT token authentication (Bearer token)
    - Environment variable configuration
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        jwt_token: Optional[str] = None
    ):
        """
        Initialize authentication handler

        Args:
            api_key: ZeroDB API key (or set ZERODB_API_KEY env var)
            jwt_token: JWT token (or set ZERODB_JWT_TOKEN env var)

        Raises:
            ValueError: If neither API key nor JWT token is provided
        """
        self.api_key = api_key or os.getenv("ZERODB_API_KEY")
        self.jwt_token = jwt_token or os.getenv("ZERODB_JWT_TOKEN")

        if not self.api_key and not self.jwt_token:
            raise ValueError(
                "Either api_key or jwt_token must be provided. "
                "Set ZERODB_API_KEY or ZERODB_JWT_TOKEN environment variable."
            )

        self._token_expiry: Optional[datetime] = None

    def get_headers(self) -> Dict[str, str]:
        """
        Get authentication headers for API requests

        Returns:
            Dictionary of HTTP headers
        """
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "zerodb-mcp-python/1.0.0"
        }

        if self.jwt_token:
            headers["Authorization"] = f"Bearer {self.jwt_token}"
        elif self.api_key:
            headers["X-API-Key"] = self.api_key

        return headers

    def update_jwt_token(self, token: str, expires_in: Optional[int] = None):
        """
        Update JWT token (useful for token refresh)

        Args:
            token: New JWT token
            expires_in: Token expiry in seconds (optional)
        """
        self.jwt_token = token
        if expires_in:
            self._token_expiry = datetime.utcnow() + timedelta(seconds=expires_in)

    def is_token_expired(self) -> bool:
        """Check if JWT token is expired"""
        if not self._token_expiry:
            return False
        return datetime.utcnow() >= self._token_expiry

    @property
    def auth_type(self) -> str:
        """Get authentication type being used"""
        if self.jwt_token:
            return "jwt"
        return "api_key"
