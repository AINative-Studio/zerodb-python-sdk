"""
Simple Memory API for ZeroDB — Issue #1414

Provides Mem0-style simple memory interface:
    db.memory.add("User prefers dark mode", user_id="alice")
    results = db.memory.search("What does the user prefer?", user_id="alice")

Wraps the /api/v1/public/memory/ endpoints with auto-embedding,
auto-categorization, and deduplication.
"""

from typing import Any, Dict, List, Optional
from uuid import uuid4


class MemoryOperations:
    """Simple memory operations — Mem0-style DX on top of ZeroDB infrastructure."""

    def __init__(self, client):
        self._client = client

    async def add(
        self,
        content: str,
        user_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Store a memory. Auto-embeds and categorizes.

        Args:
            content: The memory text (e.g., "User prefers dark mode")
            user_id: Optional user ID for scoping
            tags: Optional tags for categorization
            metadata: Optional additional metadata

        Returns:
            Dict with memory ID and status

        Example:
            await db.memory.add("User prefers dark mode", user_id="alice")
            await db.memory.add("Likes Python over JavaScript", tags=["preferences"])
        """
        meta = metadata or {}
        if user_id:
            meta["user_id"] = user_id

        # Auto entity extraction via NousCoder (Issue #1415)
        # Extracts preferences, facts, and relationships from content
        if self._client._extract_entities:
            try:
                entities = await self._extract_entities(content)
                if entities:
                    meta["extracted_entities"] = entities
                    # Auto-tag based on entity types
                    entity_tags = [e.get("type", "") for e in entities if "type" in e]
                    tags = list(set((tags or []) + entity_tags))
            except Exception:
                pass  # Entity extraction is best-effort

        body = {
            "title": content[:100],
            "content": content,
            "tags": tags or [],
            "metadata": meta,
        }

        return await self._client._request("POST", "/api/v1/public/memory/", json=body)

    async def _extract_entities(self, content: str) -> list:
        """Extract entities from memory content using NousCoder (free)."""
        try:
            response = await self._client._request(
                "POST",
                "/api/v1/chat/completions",
                json={
                    "model": "NousResearch/NousCoder-14B",
                    "messages": [
                        {
                            "role": "user",
                            "content": (
                                f"Extract entities from this text. Return JSON array of objects with "
                                f"'type' (preference/fact/relationship), 'key', and 'value' fields. "
                                f"Only return the JSON array, nothing else.\n\nText: {content}"
                            ),
                        }
                    ],
                    "max_tokens": 200,
                },
            )
            import json
            text = response.get("choices", [{}])[0].get("message", {}).get("content", "[]")
            # Parse JSON from response
            text = text.strip()
            if text.startswith("```"):
                text = text.split("\n", 1)[-1].rsplit("```", 1)[0]
            return json.loads(text)
        except Exception:
            return []

    async def search(
        self,
        query: str,
        user_id: Optional[str] = None,
        limit: int = 10,
        tags: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search memories by meaning using semantic similarity.

        Args:
            query: Natural language search query
            user_id: Optional user ID to scope search
            limit: Maximum results (default: 10)
            tags: Optional tag filter

        Returns:
            List of matching memories with similarity scores

        Example:
            results = await db.memory.search("What does the user prefer?")
            results = await db.memory.search("dark mode", user_id="alice", limit=5)
        """
        body = {
            "query": query,
            "limit": limit,
        }
        if tags:
            body["tags"] = tags

        result = await self._client._request(
            "POST", "/api/v1/public/memory/search", json=body
        )

        memories = result if isinstance(result, list) else result.get("results", result.get("data", []))

        # Filter by user_id if provided
        if user_id and isinstance(memories, list):
            memories = [
                m for m in memories
                if m.get("metadata", {}).get("user_id") == user_id
            ]

        return memories

    async def list(
        self,
        user_id: Optional[str] = None,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """
        List recent memories.

        Args:
            user_id: Optional user ID filter
            limit: Maximum results

        Returns:
            List of memories ordered by recency
        """
        params = {"limit": limit}
        result = await self._client._request(
            "GET", "/api/v1/public/memory/", params=params
        )
        memories = result if isinstance(result, list) else result.get("data", [])

        if user_id and isinstance(memories, list):
            memories = [
                m for m in memories
                if m.get("metadata", {}).get("user_id") == user_id
            ]

        return memories

    async def delete(self, memory_id: str) -> Dict[str, Any]:
        """
        Delete a specific memory.

        Args:
            memory_id: ID of the memory to delete

        Returns:
            Deletion confirmation
        """
        return await self._client._request(
            "DELETE", f"/api/v1/public/memory/{memory_id}"
        )
