"""
Pydantic models for ZeroDB MCP Client requests and responses
"""

from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, ConfigDict
from uuid import UUID


# ================================
# Vector Models
# ================================

class VectorUpsertRequest(BaseModel):
    """Request model for upserting a vector"""

    model_config = ConfigDict(str_strip_whitespace=True)

    project_id: str
    embedding: List[float] = Field(..., min_length=1, max_length=4096)
    document: str
    namespace: str = "default"
    metadata: Optional[Dict[str, Any]] = None

    @field_validator('embedding')
    @classmethod
    def validate_embedding(cls, v):
        if not all(isinstance(x, (int, float)) for x in v):
            raise ValueError("All embedding values must be numbers")
        return v


class VectorSearchRequest(BaseModel):
    """Request model for vector search"""

    model_config = ConfigDict(str_strip_whitespace=True)

    project_id: str
    query_vector: List[float] = Field(..., min_length=1, max_length=4096)
    limit: int = Field(10, ge=1, le=1000)
    threshold: float = Field(0.7, ge=0.0, le=1.0)
    namespace: Optional[str] = None


class VectorSearchResult(BaseModel):
    """Vector search result item"""

    vector_id: str
    similarity: float
    document: str
    metadata: Dict[str, Any]
    namespace: str


class BatchVectorUpsertRequest(BaseModel):
    """Request for batch vector upsert"""

    project_id: str
    vectors: List[Dict[str, Any]] = Field(..., min_length=1, max_length=1000)


# ================================
# Quantum Models
# ================================

class QuantumCompressionRequest(BaseModel):
    """Request for TurboQuant vector compression (PolarQuant + QJL)"""

    project_id: str
    vector_id: str
    target_dimensions: int = Field(..., ge=2, le=512)
    backend: str = Field("simulator", pattern="^(simulator|ionq|braket)$")


class QuantumDecompressionRequest(BaseModel):
    """Request for TurboQuant vector decompression"""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    project_id: str
    compressed_state: List[Any]  # Complex numbers represented as dicts or tuples
    original_dimensions: int


class QuantumSimilarityRequest(BaseModel):
    """Request for TurboQuant hybrid similarity search"""

    project_id: str
    query_vector: List[float]
    top_k: int = Field(10, ge=1, le=100)
    quantum_weight: float = Field(0.5, ge=0.0, le=1.0)


# ================================
# Table Models
# ================================

class TableCreateRequest(BaseModel):
    """Request to create a NoSQL table"""

    project_id: str
    table_name: str = Field(..., min_length=1, max_length=255)
    schema_definition: Dict[str, str]
    indexes: Optional[List[str]] = None


class TableRowInsertRequest(BaseModel):
    """Request to insert rows into table"""

    project_id: str
    table_name: str
    rows: List[Dict[str, Any]] = Field(..., min_length=1, max_length=1000)


class TableQueryRequest(BaseModel):
    """Request to query table rows"""

    project_id: str
    table_name: str
    filters: Optional[Dict[str, Any]] = None
    limit: int = Field(100, ge=1, le=10000)
    offset: int = Field(0, ge=0)
    sort_by: Optional[str] = None


# ================================
# File Models
# ================================

class FileUploadRequest(BaseModel):
    """Request to upload a file"""

    project_id: str
    file_name: str
    content_base64: str
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class FileResponse(BaseModel):
    """File metadata response"""

    file_id: str
    project_id: str
    file_name: str
    content_type: str
    file_size: int
    created_at: datetime
    metadata: Dict[str, Any]


# ================================
# Project Models
# ================================

class ProjectCreateRequest(BaseModel):
    """Request to create a project"""

    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    tier: str = Field("free", pattern="^(free|pro|enterprise)$")
    settings: Optional[Dict[str, Any]] = None


class ProjectUpdateRequest(BaseModel):
    """Request to update a project"""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None


class ProjectResponse(BaseModel):
    """Project response"""

    project_id: str
    name: str
    description: Optional[str]
    tier: str
    created_at: datetime
    updated_at: datetime
    settings: Dict[str, Any]


# ================================
# Event Models
# ================================

class EventCreateRequest(BaseModel):
    """Request to create an event"""

    project_id: str
    event_type: str
    event_data: Dict[str, Any]
    source: Optional[str] = "sdk"


class EventResponse(BaseModel):
    """Event response"""

    event_id: str
    project_id: str
    event_type: str
    event_data: Dict[str, Any]
    source: str
    created_at: datetime


# ================================
# RLHF Models
# ================================

class RLHFInteractionRequest(BaseModel):
    """Request to collect RLHF interaction"""

    session_id: str
    project_id: str
    interaction_type: str
    user_input: str
    agent_response: str
    context: Optional[Dict[str, Any]] = None


class RLHFFeedbackRequest(BaseModel):
    """Request to collect agent feedback"""

    session_id: str
    project_id: str
    interaction_id: str
    rating: int = Field(..., ge=1, le=5)
    feedback_text: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class RLHFWorkflowFeedbackRequest(BaseModel):
    """Request to collect workflow feedback"""

    session_id: str
    project_id: str
    workflow_id: str
    success: bool
    duration_ms: int
    error_message: Optional[str] = None


class RLHFErrorReportRequest(BaseModel):
    """Request to report an error"""

    session_id: str
    project_id: str
    error_type: str
    error_message: str
    stack_trace: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


# ================================
# Admin Models
# ================================

class SystemStatsResponse(BaseModel):
    """System statistics response"""

    total_projects: int
    total_vectors: int
    total_users: int
    storage_used_gb: float
    active_sessions: int


class UserUsageResponse(BaseModel):
    """User usage statistics"""

    user_id: str
    total_projects: int
    total_vectors: int
    total_queries: int
    storage_used_mb: float
    tier: str


# ================================
# Common Response Models
# ================================

class OperationResponse(BaseModel):
    """Generic operation response"""

    success: bool
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None


class BulkOperationResponse(BaseModel):
    """Bulk operation response"""

    total: int
    successful: int
    failed: int
    errors: Optional[List[Dict[str, Any]]] = None


class PaginatedResponse(BaseModel):
    """Paginated list response"""

    items: List[Dict[str, Any]]
    total: int
    limit: int
    offset: int
    has_more: bool
