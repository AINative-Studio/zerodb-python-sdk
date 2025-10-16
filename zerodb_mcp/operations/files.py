"""
File storage operations for ZeroDB MCP Client

Provides 6 file operations:
1. upload - Upload a file
2. download - Download a file
3. list - List files
4. delete - Delete a file
5. get_metadata - Get file metadata
6. generate_presigned_url - Generate presigned download URL
"""

from typing import Dict, Any, Optional, Union
from pathlib import Path
from ..utils import encode_file_content, decode_file_content, calculate_file_hash, build_query_params


class FileOperations:
    """File storage and management operations"""

    def __init__(self, client):
        self._client = client

    async def upload(
        self,
        project_id: str,
        file_path: Union[str, Path],
        file_name: Optional[str] = None,
        content_type: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Upload a file from local filesystem

        Args:
            project_id: Project ID
            file_path: Path to file to upload
            file_name: Optional custom file name (defaults to original name)
            content_type: MIME type (auto-detected if not provided)
            metadata: Optional metadata dict

        Returns:
            {
                "file_id": "uuid",
                "file_name": "document.pdf",
                "content_type": "application/pdf",
                "file_size": 1024000,
                "checksum": "sha256:...",
                "created_at": "..."
            }

        Example:
            >>> result = await client.files.upload(
            ...     project_id="550e8400-...",
            ...     file_path="/path/to/document.pdf",
            ...     metadata={"category": "legal", "year": 2025}
            ... )
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Read file content
        with open(file_path, 'rb') as f:
            content = f.read()

        # Use provided name or original filename
        upload_name = file_name or file_path.name

        # Auto-detect content type from extension if not provided
        if not content_type:
            content_type = self._guess_content_type(file_path.suffix)

        params = {
            "project_id": project_id,
            "file_name": upload_name,
            "content_base64": encode_file_content(content),
            "content_type": content_type,
            "metadata": metadata or {},
            "checksum": calculate_file_hash(content)
        }

        return await self._client.execute("upload_file", params)

    async def upload_bytes(
        self,
        project_id: str,
        content: bytes,
        file_name: str,
        content_type: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Upload file from bytes content

        Args:
            project_id: Project ID
            content: File content as bytes
            file_name: File name
            content_type: MIME type
            metadata: Optional metadata dict

        Returns:
            File upload result

        Example:
            >>> content = b"Hello, World!"
            >>> result = await client.files.upload_bytes(
            ...     project_id="550e8400-...",
            ...     content=content,
            ...     file_name="hello.txt",
            ...     content_type="text/plain"
            ... )
        """
        params = {
            "project_id": project_id,
            "file_name": file_name,
            "content_base64": encode_file_content(content),
            "content_type": content_type or "application/octet-stream",
            "metadata": metadata or {},
            "checksum": calculate_file_hash(content)
        }

        return await self._client.execute("upload_file", params)

    async def download(
        self,
        project_id: str,
        file_id: str,
        save_path: Optional[Union[str, Path]] = None
    ) -> Union[bytes, Dict[str, Any]]:
        """
        Download a file

        Args:
            project_id: Project ID
            file_id: File ID
            save_path: Optional path to save file (returns bytes if not provided)

        Returns:
            File bytes if save_path is None, otherwise download info dict

        Example:
            >>> # Download to memory
            >>> content = await client.files.download(
            ...     project_id="550e8400-...",
            ...     file_id="660e8400-..."
            ... )
            >>>
            >>> # Download to file
            >>> await client.files.download(
            ...     project_id="550e8400-...",
            ...     file_id="660e8400-...",
            ...     save_path="/path/to/save/file.pdf"
            ... )
        """
        params = {
            "project_id": project_id,
            "file_id": file_id
        }

        result = await self._client.execute("download_file", params)

        # Decode base64 content
        content = decode_file_content(result["content_base64"])

        if save_path:
            save_path = Path(save_path)
            save_path.parent.mkdir(parents=True, exist_ok=True)
            with open(save_path, 'wb') as f:
                f.write(content)
            return {
                "file_id": file_id,
                "saved_to": str(save_path),
                "size": len(content)
            }

        return content

    async def list(
        self,
        project_id: str,
        limit: int = 100,
        offset: int = 0,
        content_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List files in project

        Args:
            project_id: Project ID
            limit: Results per page
            offset: Number of results to skip
            content_type: Optional filter by content type

        Returns:
            {
                "files": [
                    {
                        "file_id": "uuid",
                        "file_name": "doc.pdf",
                        "content_type": "application/pdf",
                        "file_size": 1024000,
                        "created_at": "..."
                    }
                ],
                "total": 50
            }

        Example:
            >>> # List all PDFs
            >>> files = await client.files.list(
            ...     project_id="550e8400-...",
            ...     content_type="application/pdf"
            ... )
        """
        params = build_query_params(
            limit=limit,
            offset=offset,
            filters={"content_type": content_type} if content_type else None
        )
        params["project_id"] = project_id

        return await self._client.execute("list_files", params)

    async def delete(
        self,
        project_id: str,
        file_id: str
    ) -> Dict[str, Any]:
        """
        Delete a file

        Args:
            project_id: Project ID
            file_id: File ID

        Returns:
            {"status": "success"}

        Example:
            >>> await client.files.delete(
            ...     project_id="550e8400-...",
            ...     file_id="660e8400-..."
            ... )
        """
        params = {
            "project_id": project_id,
            "file_id": file_id
        }

        return await self._client.execute("delete_file", params)

    async def get_metadata(
        self,
        project_id: str,
        file_id: str
    ) -> Dict[str, Any]:
        """
        Get file metadata without downloading content

        Args:
            project_id: Project ID
            file_id: File ID

        Returns:
            {
                "file_id": "uuid",
                "file_name": "doc.pdf",
                "content_type": "application/pdf",
                "file_size": 1024000,
                "checksum": "sha256:...",
                "metadata": {...},
                "created_at": "...",
                "updated_at": "..."
            }

        Example:
            >>> metadata = await client.files.get_metadata(
            ...     project_id="550e8400-...",
            ...     file_id="660e8400-..."
            ... )
            >>> print(f"File size: {metadata['file_size']} bytes")
        """
        params = {
            "project_id": project_id,
            "file_id": file_id
        }

        return await self._client.execute("get_file_metadata", params)

    async def generate_presigned_url(
        self,
        project_id: str,
        file_id: str,
        expires_in: int = 3600
    ) -> Dict[str, Any]:
        """
        Generate presigned download URL

        Args:
            project_id: Project ID
            file_id: File ID
            expires_in: URL expiry in seconds (default: 3600 = 1 hour)

        Returns:
            {
                "url": "https://...",
                "expires_at": "2025-01-14T13:00:00Z"
            }

        Example:
            >>> result = await client.files.generate_presigned_url(
            ...     project_id="550e8400-...",
            ...     file_id="660e8400-...",
            ...     expires_in=7200  # 2 hours
            ... )
            >>> print(f"Download URL: {result['url']}")
        """
        params = {
            "project_id": project_id,
            "file_id": file_id,
            "expires_in": expires_in
        }

        return await self._client.execute("generate_presigned_url", params)

    @staticmethod
    def _guess_content_type(extension: str) -> str:
        """Guess content type from file extension"""
        content_types = {
            '.pdf': 'application/pdf',
            '.txt': 'text/plain',
            '.json': 'application/json',
            '.csv': 'text/csv',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.svg': 'image/svg+xml',
            '.mp4': 'video/mp4',
            '.mp3': 'audio/mpeg',
            '.wav': 'audio/wav',
            '.zip': 'application/zip',
            '.tar': 'application/x-tar',
            '.gz': 'application/gzip',
        }
        return content_types.get(extension.lower(), 'application/octet-stream')
