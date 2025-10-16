"""
File upload and management example for ZeroDB MCP Python Client
"""

import asyncio
from pathlib import Path
from zerodb_mcp import ZeroDBClient


async def main():
    client = ZeroDBClient(api_key="your_api_key_here")

    try:
        project_id = "your_project_id_here"

        # 1. Upload a file from local filesystem
        print("1. Uploading file...")
        upload_result = await client.files.upload(
            project_id=project_id,
            file_path="/path/to/document.pdf",
            metadata={
                "category": "legal",
                "year": 2025,
                "confidential": False
            }
        )
        file_id = upload_result["file_id"]
        print(f"Uploaded file: {file_id}")
        print(f"Size: {upload_result['file_size']:,} bytes")

        # 2. Upload bytes content
        print("\n2. Uploading bytes content...")
        content = b"Hello, World! This is test content."
        bytes_result = await client.files.upload_bytes(
            project_id=project_id,
            content=content,
            file_name="hello.txt",
            content_type="text/plain",
            metadata={"type": "greeting"}
        )
        print(f"Uploaded: {bytes_result['file_name']}")

        # 3. List files
        print("\n3. Listing files...")
        files = await client.files.list(
            project_id=project_id,
            limit=10
        )
        print(f"Total files: {files['total']}")
        for file in files['files']:
            print(f"- {file['file_name']} ({file['file_size']:,} bytes)")

        # 4. Get file metadata
        print("\n4. Getting file metadata...")
        metadata = await client.files.get_metadata(project_id, file_id)
        print(f"File: {metadata['file_name']}")
        print(f"Type: {metadata['content_type']}")
        print(f"Created: {metadata['created_at']}")

        # 5. Generate presigned URL
        print("\n5. Generating download URL...")
        url_result = await client.files.generate_presigned_url(
            project_id=project_id,
            file_id=file_id,
            expires_in=3600  # 1 hour
        )
        print(f"Download URL: {url_result['url']}")
        print(f"Expires at: {url_result['expires_at']}")

        # 6. Download file
        print("\n6. Downloading file...")
        content = await client.files.download(project_id, file_id)
        print(f"Downloaded {len(content)} bytes")

        # Or save directly to file
        save_path = Path("./downloaded_file.pdf")
        await client.files.download(
            project_id=project_id,
            file_id=file_id,
            save_path=save_path
        )
        print(f"Saved to: {save_path}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
