"""
Basic usage example for ZeroDB MCP Python Client
"""

import asyncio
from zerodb_mcp import ZeroDBClient


async def main():
    # Initialize client with API key
    client = ZeroDBClient(api_key="your_api_key_here")

    try:
        # Check API health
        health = await client.health_check()
        print(f"API Health: {health}")

        # Create a project
        print("\n1. Creating project...")
        project = await client.projects.create(
            name="Example Project",
            description="Testing the Python SDK",
            tier="free"
        )
        project_id = project["project_id"]
        print(f"Created project: {project_id}")

        # Upsert a vector
        print("\n2. Upserting vector...")
        vector_result = await client.vectors.upsert(
            project_id=project_id,
            embedding=[0.1] * 1536,  # Example 1536-dimensional vector
            document="This is a sample document about machine learning",
            metadata={"category": "AI", "language": "en"}
        )
        print(f"Vector upserted: {vector_result['vector_id']}")

        # Search vectors
        print("\n3. Searching vectors...")
        search_results = await client.vectors.search(
            project_id=project_id,
            query_vector=[0.1] * 1536,
            limit=5,
            threshold=0.7
        )
        print(f"Found {len(search_results['results'])} results")

        # Get project statistics
        print("\n4. Getting project stats...")
        stats = await client.projects.get_stats(project_id)
        print(f"Project stats: {stats}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the client
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
