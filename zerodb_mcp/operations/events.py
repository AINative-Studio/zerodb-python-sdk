"""
Event operations for ZeroDB MCP Client

Provides 5 event operations:
1. create - Create an event
2. list - List events
3. get - Get event details
4. subscribe - Subscribe to event stream
5. stats - Get event statistics
"""

from typing import Dict, Any, Optional, AsyncIterator
from ..utils import build_query_params


class EventOperations:
    """Event tracking and streaming operations"""

    def __init__(self, client):
        self._client = client

    async def create(
        self,
        project_id: str,
        event_type: str,
        event_data: Dict[str, Any],
        source: str = "sdk"
    ) -> Dict[str, Any]:
        """
        Create an event

        Args:
            project_id: Project ID
            event_type: Event type (e.g., "user.login", "vector.search")
            event_data: Event data payload
            source: Event source (default: "sdk")

        Returns:
            {
                "event_id": "uuid",
                "event_type": "user.login",
                "created_at": "..."
            }

        Example:
            >>> event = await client.events.create(
            ...     project_id="550e8400-...",
            ...     event_type="user.login",
            ...     event_data={
            ...         "user_id": "user123",
            ...         "ip": "192.168.1.1",
            ...         "timestamp": "2025-01-14T12:00:00Z"
            ...     }
            ... )
        """
        params = {
            "project_id": project_id,
            "event_type": event_type,
            "event_data": event_data,
            "source": source
        }

        return await self._client.execute("create_event", params)

    async def list(
        self,
        project_id: str,
        event_type: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List events

        Args:
            project_id: Project ID
            event_type: Optional filter by event type
            limit: Results per page
            offset: Number of results to skip
            start_date: Optional start date (ISO format)
            end_date: Optional end date (ISO format)

        Returns:
            {
                "events": [
                    {
                        "event_id": "uuid",
                        "event_type": "user.login",
                        "event_data": {...},
                        "created_at": "..."
                    }
                ],
                "total": 1000
            }

        Example:
            >>> events = await client.events.list(
            ...     project_id="550e8400-...",
            ...     event_type="user.login",
            ...     start_date="2025-01-01T00:00:00Z",
            ...     limit=50
            ... )
        """
        filters = {}
        if event_type:
            filters["event_type"] = event_type
        if start_date:
            filters["start_date"] = start_date
        if end_date:
            filters["end_date"] = end_date

        params = build_query_params(
            limit=limit,
            offset=offset,
            filters=filters if filters else None
        )
        params["project_id"] = project_id

        return await self._client.execute("list_events", params)

    async def get(
        self,
        project_id: str,
        event_id: str
    ) -> Dict[str, Any]:
        """
        Get event details

        Args:
            project_id: Project ID
            event_id: Event ID

        Returns:
            {
                "event_id": "uuid",
                "event_type": "user.login",
                "event_data": {...},
                "source": "sdk",
                "created_at": "..."
            }

        Example:
            >>> event = await client.events.get(
            ...     project_id="550e8400-...",
            ...     event_id="660e8400-..."
            ... )
        """
        params = {
            "project_id": project_id,
            "event_id": event_id
        }

        return await self._client.execute("get_event", params)

    async def subscribe(
        self,
        project_id: str,
        event_types: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Subscribe to event stream

        Note: This creates a subscription. Use WebSocket for real-time streaming.

        Args:
            project_id: Project ID
            event_types: Optional list of event types to subscribe to

        Returns:
            {
                "subscription_id": "uuid",
                "websocket_url": "wss://...",
                "event_types": ["user.login", "vector.search"]
            }

        Example:
            >>> sub = await client.events.subscribe(
            ...     project_id="550e8400-...",
            ...     event_types=["user.login", "user.logout"]
            ... )
            >>> # Connect to websocket_url for real-time events
        """
        params = {
            "project_id": project_id
        }

        if event_types:
            params["event_types"] = event_types

        return await self._client.execute("subscribe_to_events", params)

    async def stats(
        self,
        project_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get event statistics

        Args:
            project_id: Project ID
            start_date: Optional start date (ISO format)
            end_date: Optional end date (ISO format)

        Returns:
            {
                "total_events": 10000,
                "by_type": {
                    "user.login": 5000,
                    "vector.search": 3000,
                    "file.upload": 2000
                },
                "by_source": {
                    "sdk": 8000,
                    "api": 2000
                },
                "period": {
                    "start": "2025-01-01T00:00:00Z",
                    "end": "2025-01-14T23:59:59Z"
                }
            }

        Example:
            >>> stats = await client.events.stats(
            ...     project_id="550e8400-...",
            ...     start_date="2025-01-01T00:00:00Z"
            ... )
            >>> for event_type, count in stats['by_type'].items():
            ...     print(f"{event_type}: {count}")
        """
        params = {"project_id": project_id}

        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        return await self._client.execute("event_stats", params)
