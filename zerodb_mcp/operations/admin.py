"""
Admin operations for ZeroDB MCP Client

Provides 5 admin operations (requires admin privileges):
1. get_system_stats - Get system statistics
2. list_all_projects - List all projects (admin only)
3. get_user_usage - Get user usage statistics
4. system_health - Check system health
5. optimize_database - Optimize database
"""

from typing import Dict, Any, Optional
from ..utils import build_query_params


class AdminOperations:
    """Administrative operations (requires admin privileges)"""

    def __init__(self, client):
        self._client = client

    async def get_system_stats(self) -> Dict[str, Any]:
        """
        Get system-wide statistics

        Requires: Admin privileges

        Returns:
            {
                "total_users": 1000,
                "total_projects": 5000,
                "total_vectors": 10000000,
                "total_storage_gb": 500.0,
                "active_sessions": 150,
                "api_calls_today": 50000,
                "quantum_executions_today": 100
            }

        Example:
            >>> stats = await client.admin.get_system_stats()
            >>> print(f"Total users: {stats['total_users']}")
            >>> print(f"Total vectors: {stats['total_vectors']:,}")
        """
        params = {}
        return await self._client.execute("admin_get_system_stats", params)

    async def list_all_projects(
        self,
        limit: int = 100,
        offset: int = 0,
        tier: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List all projects (admin only)

        Requires: Admin privileges

        Args:
            limit: Results per page
            offset: Number of results to skip
            tier: Optional filter by tier
            user_id: Optional filter by user

        Returns:
            {
                "projects": [
                    {
                        "project_id": "uuid",
                        "name": "Project Name",
                        "user_id": "uuid",
                        "tier": "pro",
                        "created_at": "...",
                        "stats": {...}
                    }
                ],
                "total": 5000
            }

        Example:
            >>> projects = await client.admin.list_all_projects(
            ...     tier="enterprise",
            ...     limit=50
            ... )
        """
        filters = {}
        if tier:
            filters["tier"] = tier
        if user_id:
            filters["user_id"] = user_id

        params = build_query_params(
            limit=limit,
            offset=offset,
            filters=filters if filters else None
        )

        return await self._client.execute("admin_list_all_projects", params)

    async def get_user_usage(
        self,
        user_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get user usage statistics

        Requires: Admin privileges

        Args:
            user_id: User ID
            start_date: Optional start date (ISO format)
            end_date: Optional end date (ISO format)

        Returns:
            {
                "user_id": "uuid",
                "total_projects": 10,
                "total_vectors": 50000,
                "total_queries": 100000,
                "storage_used_gb": 5.5,
                "api_calls": 150000,
                "quantum_executions": 500,
                "tier": "pro",
                "quota_usage": {
                    "vectors": {"used": 50000, "limit": 100000},
                    "storage_gb": {"used": 5.5, "limit": 10.0}
                }
            }

        Example:
            >>> usage = await client.admin.get_user_usage(
            ...     user_id="user_123",
            ...     start_date="2025-01-01T00:00:00Z"
            ... )
            >>> print(f"Vectors used: {usage['quota_usage']['vectors']['used']}")
        """
        params = {"user_id": user_id}

        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        return await self._client.execute("admin_get_user_usage", params)

    async def system_health(self) -> Dict[str, Any]:
        """
        Check system health

        Requires: Admin privileges

        Returns:
            {
                "status": "healthy",
                "database": {
                    "status": "healthy",
                    "connection_pool": {"active": 10, "idle": 5}
                },
                "quantum_backend": {
                    "status": "healthy",
                    "available_devices": ["ionq.qpu", "simulator"]
                },
                "storage": {
                    "status": "healthy",
                    "available_gb": 1000.0,
                    "used_gb": 500.0
                },
                "api": {
                    "status": "healthy",
                    "requests_per_second": 100
                },
                "uptime_seconds": 86400
            }

        Example:
            >>> health = await client.admin.system_health()
            >>> if health['status'] == 'healthy':
            ...     print("All systems operational")
            >>> else:
            ...     print(f"System issues detected: {health}")
        """
        params = {}
        return await self._client.execute("admin_system_health", params)

    async def optimize_database(
        self,
        vacuum: bool = True,
        reindex: bool = True,
        analyze: bool = True
    ) -> Dict[str, Any]:
        """
        Optimize database performance

        Requires: Admin privileges

        Args:
            vacuum: Run VACUUM to reclaim storage
            reindex: Rebuild indexes
            analyze: Update statistics

        Returns:
            {
                "status": "success",
                "operations_performed": ["vacuum", "reindex", "analyze"],
                "space_freed_gb": 5.5,
                "duration_seconds": 120,
                "completed_at": "..."
            }

        Example:
            >>> result = await client.admin.optimize_database(
            ...     vacuum=True,
            ...     reindex=True,
            ...     analyze=True
            ... )
            >>> print(f"Space freed: {result['space_freed_gb']:.2f} GB")
        """
        params = {
            "vacuum": vacuum,
            "reindex": reindex,
            "analyze": analyze
        }

        return await self._client.execute("admin_optimize_database", params)
