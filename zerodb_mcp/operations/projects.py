"""
Project management operations for ZeroDB MCP Client

Provides 7 project operations:
1. create - Create a new project
2. get - Get project details
3. list - List user's projects
4. update - Update project settings
5. delete - Delete a project
6. get_stats - Get project statistics
7. enable_database - Enable database features
"""

from typing import Dict, Any, Optional
from ..utils import validate_tier, build_query_params


class ProjectOperations:
    """Project management operations"""

    def __init__(self, client):
        self._client = client

    async def create(
        self,
        name: str,
        description: Optional[str] = None,
        tier: str = "free",
        settings: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a new project

        Args:
            name: Project name
            description: Optional description
            tier: Project tier (free, pro, enterprise)
            settings: Optional project settings

        Returns:
            {
                "project_id": "uuid",
                "name": "My Project",
                "tier": "pro",
                "created_at": "...",
                "api_key": "..."
            }

        Example:
            >>> project = await client.projects.create(
            ...     name="AI Assistant Project",
            ...     description="Semantic search for documentation",
            ...     tier="pro",
            ...     settings={
            ...         "vector_dimensions": 1536,
            ...         "enable_quantum": True
            ...     }
            ... )
            >>> print(f"Project ID: {project['project_id']}")
            >>> print(f"API Key: {project['api_key']}")
        """
        validate_tier(tier)

        params = {
            "name": name,
            "tier": tier
        }

        if description:
            params["description"] = description

        if settings:
            params["settings"] = settings

        return await self._client.execute("create_project", params)

    async def get(
        self,
        project_id: str
    ) -> Dict[str, Any]:
        """
        Get project details

        Args:
            project_id: Project ID

        Returns:
            {
                "project_id": "uuid",
                "name": "My Project",
                "description": "...",
                "tier": "pro",
                "settings": {...},
                "created_at": "...",
                "updated_at": "..."
            }

        Example:
            >>> project = await client.projects.get(
            ...     project_id="550e8400-..."
            ... )
        """
        params = {"project_id": project_id}
        return await self._client.execute("get_project", params)

    async def list(
        self,
        limit: int = 100,
        offset: int = 0,
        tier: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List user's projects

        Args:
            limit: Results per page
            offset: Number of results to skip
            tier: Optional filter by tier

        Returns:
            {
                "projects": [
                    {
                        "project_id": "uuid",
                        "name": "Project 1",
                        "tier": "pro",
                        "created_at": "..."
                    }
                ],
                "total": 5
            }

        Example:
            >>> projects = await client.projects.list(tier="pro")
            >>> for proj in projects["projects"]:
            ...     print(f"{proj['name']}: {proj['tier']}")
        """
        params = build_query_params(
            limit=limit,
            offset=offset,
            filters={"tier": tier} if tier else None
        )

        return await self._client.execute("list_projects", params)

    async def update(
        self,
        project_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        settings: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Update project settings

        Args:
            project_id: Project ID
            name: New project name (optional)
            description: New description (optional)
            settings: Updated settings (optional)

        Returns:
            {
                "project_id": "uuid",
                "updated_fields": ["name", "settings"],
                "updated_at": "..."
            }

        Example:
            >>> result = await client.projects.update(
            ...     project_id="550e8400-...",
            ...     name="Updated Project Name",
            ...     settings={"enable_quantum": False}
            ... )
        """
        params = {"project_id": project_id}

        if name:
            params["name"] = name
        if description is not None:
            params["description"] = description
        if settings:
            params["settings"] = settings

        if len(params) == 1:
            raise ValueError("At least one field to update must be provided")

        return await self._client.execute("update_project", params)

    async def delete(
        self,
        project_id: str,
        confirm: bool = False
    ) -> Dict[str, Any]:
        """
        Delete a project and all its data

        CAUTION: This permanently deletes all vectors, tables, files, and events.

        Args:
            project_id: Project ID
            confirm: Must be True to confirm deletion

        Returns:
            {
                "status": "success",
                "deleted_items": {
                    "vectors": 1000,
                    "tables": 5,
                    "files": 20
                }
            }

        Example:
            >>> result = await client.projects.delete(
            ...     project_id="550e8400-...",
            ...     confirm=True
            ... )
        """
        if not confirm:
            raise ValueError("Must set confirm=True to delete project")

        params = {
            "project_id": project_id,
            "confirm": True
        }

        return await self._client.execute("delete_project", params)

    async def get_stats(
        self,
        project_id: str
    ) -> Dict[str, Any]:
        """
        Get project statistics

        Args:
            project_id: Project ID

        Returns:
            {
                "project_id": "uuid",
                "vectors": {
                    "total": 10000,
                    "namespaces": 3,
                    "storage_mb": 125.5
                },
                "tables": {
                    "total": 5,
                    "total_rows": 50000
                },
                "files": {
                    "total": 20,
                    "storage_mb": 500.0
                },
                "queries_this_month": 15000,
                "api_calls_this_month": 25000
            }

        Example:
            >>> stats = await client.projects.get_stats(
            ...     project_id="550e8400-..."
            ... )
            >>> print(f"Total vectors: {stats['vectors']['total']}")
            >>> print(f"Storage used: {stats['vectors']['storage_mb']:.2f} MB")
        """
        params = {"project_id": project_id}
        return await self._client.execute("get_project_stats", params)

    async def enable_database(
        self,
        project_id: str,
        database_type: str = "postgres",
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Enable database features for project

        Args:
            project_id: Project ID
            database_type: Database type (postgres, mysql, mongodb)
            config: Optional database configuration

        Returns:
            {
                "status": "success",
                "database_type": "postgres",
                "connection_string": "postgresql://...",
                "enabled_at": "..."
            }

        Example:
            >>> result = await client.projects.enable_database(
            ...     project_id="550e8400-...",
            ...     database_type="postgres",
            ...     config={"pool_size": 10}
            ... )
        """
        valid_types = ["postgres", "mysql", "mongodb"]
        if database_type not in valid_types:
            raise ValueError(f"database_type must be one of {valid_types}")

        params = {
            "project_id": project_id,
            "database_type": database_type
        }

        if config:
            params["config"] = config

        return await self._client.execute("enable_database", params)
