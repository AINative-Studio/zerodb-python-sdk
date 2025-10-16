"""
NoSQL table operations for ZeroDB MCP Client

Provides 8 table operations:
1. create - Create a new table
2. list - List all tables
3. get - Get table details
4. delete - Delete a table
5. insert_rows - Insert rows into table
6. query_rows - Query table rows
7. update_rows - Update rows
8. delete_rows - Delete rows
"""

from typing import Dict, Any, List, Optional
from ..utils import build_query_params


class TableOperations:
    """NoSQL table operations for flexible data storage"""

    def __init__(self, client):
        self._client = client

    async def create(
        self,
        project_id: str,
        table_name: str,
        schema_definition: Dict[str, str],
        indexes: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Create a new NoSQL table

        Args:
            project_id: Project ID
            table_name: Table name (unique within project)
            schema_definition: Schema dict mapping field names to types
                (e.g., {"name": "string", "age": "integer", "tags": "array"})
            indexes: Optional list of fields to index

        Returns:
            {
                "table_id": "uuid",
                "table_name": "users",
                "schema": {...},
                "created_at": "2025-01-14T..."
            }

        Example:
            >>> table = await client.tables.create(
            ...     project_id="550e8400-...",
            ...     table_name="users",
            ...     schema_definition={
            ...         "user_id": "string",
            ...         "email": "string",
            ...         "age": "integer",
            ...         "tags": "array",
            ...         "metadata": "object"
            ...     },
            ...     indexes=["user_id", "email"]
            ... )
        """
        if not table_name:
            raise ValueError("table_name cannot be empty")

        if not schema_definition:
            raise ValueError("schema_definition cannot be empty")

        params = {
            "project_id": project_id,
            "table_name": table_name,
            "schema_definition": schema_definition,
            "indexes": indexes or []
        }

        return await self._client.execute("create_table", params)

    async def list(
        self,
        project_id: str,
        limit: int = 100,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        List all tables in project

        Args:
            project_id: Project ID
            limit: Results per page
            offset: Number of results to skip

        Returns:
            {
                "tables": [
                    {
                        "table_id": "uuid",
                        "table_name": "users",
                        "row_count": 1000,
                        "created_at": "..."
                    }
                ],
                "total": 5
            }

        Example:
            >>> tables = await client.tables.list(
            ...     project_id="550e8400-..."
            ... )
            >>> for table in tables["tables"]:
            ...     print(f"{table['table_name']}: {table['row_count']} rows")
        """
        params = build_query_params(limit=limit, offset=offset)
        params["project_id"] = project_id

        return await self._client.execute("list_tables", params)

    async def get(
        self,
        project_id: str,
        table_name: str
    ) -> Dict[str, Any]:
        """
        Get table details

        Args:
            project_id: Project ID
            table_name: Table name

        Returns:
            {
                "table_id": "uuid",
                "table_name": "users",
                "schema": {...},
                "indexes": [...],
                "row_count": 1000,
                "created_at": "...",
                "updated_at": "..."
            }

        Example:
            >>> table = await client.tables.get(
            ...     project_id="550e8400-...",
            ...     table_name="users"
            ... )
        """
        params = {
            "project_id": project_id,
            "table_name": table_name
        }

        return await self._client.execute("get_table", params)

    async def delete(
        self,
        project_id: str,
        table_name: str
    ) -> Dict[str, Any]:
        """
        Delete a table and all its data

        Args:
            project_id: Project ID
            table_name: Table name

        Returns:
            {"status": "success", "rows_deleted": 1000}

        Example:
            >>> await client.tables.delete(
            ...     project_id="550e8400-...",
            ...     table_name="old_table"
            ... )
        """
        params = {
            "project_id": project_id,
            "table_name": table_name
        }

        return await self._client.execute("delete_table", params)

    async def insert_rows(
        self,
        project_id: str,
        table_name: str,
        rows: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Insert rows into table

        Args:
            project_id: Project ID
            table_name: Table name
            rows: List of row dicts (max 1000 per request)

        Returns:
            {
                "inserted": 100,
                "failed": 0,
                "row_ids": ["id1", "id2", ...]
            }

        Example:
            >>> rows = [
            ...     {"user_id": "u1", "email": "user1@example.com", "age": 25},
            ...     {"user_id": "u2", "email": "user2@example.com", "age": 30}
            ... ]
            >>> result = await client.tables.insert_rows(
            ...     project_id="550e8400-...",
            ...     table_name="users",
            ...     rows=rows
            ... )
        """
        if not rows:
            raise ValueError("rows cannot be empty")

        if len(rows) > 1000:
            raise ValueError("Maximum 1000 rows per request")

        params = {
            "project_id": project_id,
            "table_name": table_name,
            "rows": rows
        }

        return await self._client.execute("insert_rows", params)

    async def query_rows(
        self,
        project_id: str,
        table_name: str,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 100,
        offset: int = 0,
        sort_by: Optional[str] = None,
        order: str = "asc"
    ) -> Dict[str, Any]:
        """
        Query table rows

        Args:
            project_id: Project ID
            table_name: Table name
            filters: Query filters (e.g., {"age": {"$gte": 18}})
            limit: Results per page
            offset: Number of results to skip
            sort_by: Field to sort by
            order: Sort order ('asc' or 'desc')

        Returns:
            {
                "rows": [...],
                "total": 1000,
                "limit": 100,
                "offset": 0
            }

        Example:
            >>> # Query users over 18
            >>> results = await client.tables.query_rows(
            ...     project_id="550e8400-...",
            ...     table_name="users",
            ...     filters={"age": {"$gte": 18}},
            ...     sort_by="age",
            ...     order="desc"
            ... )
        """
        params = {
            "project_id": project_id,
            "table_name": table_name,
            "filters": filters or {},
            "limit": limit,
            "offset": offset
        }

        if sort_by:
            params["sort_by"] = sort_by
            params["order"] = order

        return await self._client.execute("query_rows", params)

    async def update_rows(
        self,
        project_id: str,
        table_name: str,
        filters: Dict[str, Any],
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update rows matching filters

        Args:
            project_id: Project ID
            table_name: Table name
            filters: Filters to match rows
            updates: Fields to update

        Returns:
            {"updated": 10}

        Example:
            >>> # Update all users over 18
            >>> result = await client.tables.update_rows(
            ...     project_id="550e8400-...",
            ...     table_name="users",
            ...     filters={"age": {"$gte": 18}},
            ...     updates={"verified": True}
            ... )
        """
        params = {
            "project_id": project_id,
            "table_name": table_name,
            "filters": filters,
            "updates": updates
        }

        return await self._client.execute("update_rows", params)

    async def delete_rows(
        self,
        project_id: str,
        table_name: str,
        filters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Delete rows matching filters

        Args:
            project_id: Project ID
            table_name: Table name
            filters: Filters to match rows to delete

        Returns:
            {"deleted": 5}

        Example:
            >>> # Delete inactive users
            >>> result = await client.tables.delete_rows(
            ...     project_id="550e8400-...",
            ...     table_name="users",
            ...     filters={"last_login": {"$lt": "2024-01-01"}}
            ... )
        """
        params = {
            "project_id": project_id,
            "table_name": table_name,
            "filters": filters
        }

        return await self._client.execute("delete_rows", params)
