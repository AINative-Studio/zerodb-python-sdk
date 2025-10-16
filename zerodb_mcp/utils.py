"""
Utility functions for ZeroDB MCP Client
"""

import base64
import hashlib
import json
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
from uuid import UUID


def validate_uuid(value: str) -> bool:
    """Validate UUID string format"""
    try:
        UUID(value)
        return True
    except (ValueError, AttributeError):
        return False


def validate_embedding(embedding: List[float], max_dimensions: int = 4096) -> None:
    """
    Validate vector embedding

    Args:
        embedding: List of floats
        max_dimensions: Maximum allowed dimensions

    Raises:
        ValueError: If embedding is invalid
    """
    if not isinstance(embedding, list):
        raise ValueError("Embedding must be a list")

    if not embedding:
        raise ValueError("Embedding cannot be empty")

    if len(embedding) > max_dimensions:
        raise ValueError(f"Embedding exceeds maximum dimensions ({max_dimensions})")

    if not all(isinstance(x, (int, float)) for x in embedding):
        raise ValueError("All embedding values must be numbers")


def encode_file_content(content: bytes) -> str:
    """
    Encode file content to base64 string

    Args:
        content: File content as bytes

    Returns:
        Base64 encoded string
    """
    return base64.b64encode(content).decode('utf-8')


def decode_file_content(encoded: str) -> bytes:
    """
    Decode base64 file content

    Args:
        encoded: Base64 encoded string

    Returns:
        Original bytes
    """
    return base64.b64decode(encoded.encode('utf-8'))


def calculate_file_hash(content: bytes) -> str:
    """Calculate SHA256 hash of file content"""
    return hashlib.sha256(content).hexdigest()


def sanitize_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitize metadata dict for JSON serialization

    Converts non-serializable types to strings
    """
    sanitized = {}
    for key, value in metadata.items():
        if isinstance(value, (str, int, float, bool, type(None))):
            sanitized[key] = value
        elif isinstance(value, (list, tuple)):
            sanitized[key] = [
                v if isinstance(v, (str, int, float, bool, type(None))) else str(v)
                for v in value
            ]
        elif isinstance(value, dict):
            sanitized[key] = sanitize_metadata(value)
        elif isinstance(value, datetime):
            sanitized[key] = value.isoformat()
        elif isinstance(value, UUID):
            sanitized[key] = str(value)
        else:
            sanitized[key] = str(value)
    return sanitized


def build_query_params(
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    sort_by: Optional[str] = None,
    order: Optional[str] = None,
    filters: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Build query parameters for list operations

    Args:
        limit: Maximum number of results
        offset: Number of results to skip
        sort_by: Field to sort by
        order: Sort order ('asc' or 'desc')
        filters: Additional filters

    Returns:
        Query parameters dict
    """
    params = {}

    if limit is not None:
        params['limit'] = limit
    if offset is not None:
        params['offset'] = offset
    if sort_by:
        params['sort_by'] = sort_by
    if order:
        params['order'] = order
    if filters:
        params.update(filters)

    return params


def format_error_message(response_data: Dict[str, Any]) -> str:
    """
    Format error message from API response

    Args:
        response_data: API error response

    Returns:
        Formatted error message
    """
    if 'detail' in response_data:
        detail = response_data['detail']
        if isinstance(detail, str):
            return detail
        if isinstance(detail, list):
            return '; '.join(
                f"{err.get('loc', ['unknown'])[0]}: {err.get('msg', 'error')}"
                for err in detail
            )
        if isinstance(detail, dict):
            return json.dumps(detail, indent=2)

    return response_data.get('message', 'Unknown error')


def chunk_list(items: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Split list into chunks

    Args:
        items: List to split
        chunk_size: Size of each chunk

    Returns:
        List of chunks
    """
    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]


def validate_tier(tier: str) -> None:
    """
    Validate project tier

    Args:
        tier: Tier name

    Raises:
        ValueError: If tier is invalid
    """
    valid_tiers = ['free', 'pro', 'enterprise']
    if tier.lower() not in valid_tiers:
        raise ValueError(f"Invalid tier. Must be one of: {', '.join(valid_tiers)}")


def parse_retry_after(retry_after: Union[str, int, None]) -> Optional[int]:
    """
    Parse Retry-After header value

    Args:
        retry_after: Retry-After header value (seconds or HTTP date)

    Returns:
        Retry delay in seconds
    """
    if retry_after is None:
        return None

    if isinstance(retry_after, int):
        return retry_after

    try:
        return int(retry_after)
    except (ValueError, TypeError):
        # Could be HTTP date format - simplified to 60 seconds default
        return 60
