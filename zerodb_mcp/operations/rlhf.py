"""
RLHF (Reinforcement Learning from Human Feedback) operations for ZeroDB MCP Client

Provides 10 RLHF operations:
1. collect_interaction - Collect user-agent interaction
2. collect_agent_feedback - Collect feedback on agent response
3. collect_workflow_feedback - Collect workflow completion feedback
4. collect_error_report - Report errors and issues
5. get_status - Get RLHF collection status
6. get_summary - Get feedback summary
7. start_collection - Start RLHF collection session
8. stop_collection - Stop RLHF collection session
9. get_session_interactions - Get interactions for a session
10. broadcast_event - Broadcast RLHF event
"""

from typing import Dict, Any, Optional


class RLHFOperations:
    """RLHF feedback collection operations"""

    def __init__(self, client):
        self._client = client

    async def collect_interaction(
        self,
        session_id: str,
        project_id: str,
        interaction_type: str,
        user_input: str,
        agent_response: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Collect user-agent interaction for RLHF

        Args:
            session_id: Session ID
            project_id: Project ID
            interaction_type: Type of interaction (query, command, conversation)
            user_input: User's input/query
            agent_response: Agent's response
            context: Optional context data

        Returns:
            {
                "interaction_id": "uuid",
                "session_id": "...",
                "created_at": "..."
            }

        Example:
            >>> interaction = await client.rlhf.collect_interaction(
            ...     session_id="sess_123",
            ...     project_id="550e8400-...",
            ...     interaction_type="query",
            ...     user_input="What is quantum computing?",
            ...     agent_response="Quantum computing is...",
            ...     context={"model": "gpt-4", "tokens": 150}
            ... )
        """
        params = {
            "session_id": session_id,
            "project_id": project_id,
            "interaction_type": interaction_type,
            "user_input": user_input,
            "agent_response": agent_response,
            "context": context or {}
        }

        return await self._client.execute("rlhf_collect_interaction", params)

    async def collect_agent_feedback(
        self,
        session_id: str,
        project_id: str,
        interaction_id: str,
        rating: int,
        feedback_text: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Collect user feedback on agent response

        Args:
            session_id: Session ID
            project_id: Project ID
            interaction_id: Interaction ID being rated
            rating: Rating (1-5)
            feedback_text: Optional feedback text
            metadata: Optional metadata

        Returns:
            {
                "feedback_id": "uuid",
                "interaction_id": "...",
                "created_at": "..."
            }

        Example:
            >>> feedback = await client.rlhf.collect_agent_feedback(
            ...     session_id="sess_123",
            ...     project_id="550e8400-...",
            ...     interaction_id="int_456",
            ...     rating=5,
            ...     feedback_text="Very helpful and accurate response",
            ...     metadata={"helpful": True, "accurate": True}
            ... )
        """
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")

        params = {
            "session_id": session_id,
            "project_id": project_id,
            "interaction_id": interaction_id,
            "rating": rating
        }

        if feedback_text:
            params["feedback_text"] = feedback_text
        if metadata:
            params["metadata"] = metadata

        return await self._client.execute("rlhf_collect_agent_feedback", params)

    async def collect_workflow_feedback(
        self,
        session_id: str,
        project_id: str,
        workflow_id: str,
        success: bool,
        duration_ms: int,
        error_message: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Collect workflow completion feedback

        Args:
            session_id: Session ID
            project_id: Project ID
            workflow_id: Workflow identifier
            success: Whether workflow completed successfully
            duration_ms: Workflow duration in milliseconds
            error_message: Error message if failed
            metadata: Optional metadata

        Returns:
            {
                "feedback_id": "uuid",
                "workflow_id": "...",
                "created_at": "..."
            }

        Example:
            >>> feedback = await client.rlhf.collect_workflow_feedback(
            ...     session_id="sess_123",
            ...     project_id="550e8400-...",
            ...     workflow_id="workflow_search",
            ...     success=True,
            ...     duration_ms=250,
            ...     metadata={"results_found": 10}
            ... )
        """
        params = {
            "session_id": session_id,
            "project_id": project_id,
            "workflow_id": workflow_id,
            "success": success,
            "duration_ms": duration_ms
        }

        if error_message:
            params["error_message"] = error_message
        if metadata:
            params["metadata"] = metadata

        return await self._client.execute("rlhf_collect_workflow_feedback", params)

    async def collect_error_report(
        self,
        session_id: str,
        project_id: str,
        error_type: str,
        error_message: str,
        stack_trace: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Report error for RLHF analysis

        Args:
            session_id: Session ID
            project_id: Project ID
            error_type: Error type/category
            error_message: Error message
            stack_trace: Optional stack trace
            context: Optional context data

        Returns:
            {
                "error_id": "uuid",
                "session_id": "...",
                "created_at": "..."
            }

        Example:
            >>> error = await client.rlhf.collect_error_report(
            ...     session_id="sess_123",
            ...     project_id="550e8400-...",
            ...     error_type="ValidationError",
            ...     error_message="Invalid vector dimensions",
            ...     stack_trace="Traceback...",
            ...     context={"operation": "upsert_vector"}
            ... )
        """
        params = {
            "session_id": session_id,
            "project_id": project_id,
            "error_type": error_type,
            "error_message": error_message
        }

        if stack_trace:
            params["stack_trace"] = stack_trace
        if context:
            params["context"] = context

        return await self._client.execute("rlhf_collect_error_report", params)

    async def get_status(
        self,
        project_id: str
    ) -> Dict[str, Any]:
        """
        Get RLHF collection status

        Args:
            project_id: Project ID

        Returns:
            {
                "enabled": True,
                "active_sessions": 5,
                "total_interactions": 1000,
                "total_feedback": 800,
                "average_rating": 4.2
            }

        Example:
            >>> status = await client.rlhf.get_status(
            ...     project_id="550e8400-..."
            ... )
            >>> print(f"Average rating: {status['average_rating']}")
        """
        params = {"project_id": project_id}
        return await self._client.execute("rlhf_get_status", params)

    async def get_summary(
        self,
        project_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get RLHF feedback summary

        Args:
            project_id: Project ID
            start_date: Optional start date (ISO format)
            end_date: Optional end date (ISO format)

        Returns:
            {
                "total_interactions": 1000,
                "total_feedback": 800,
                "rating_distribution": {
                    "1": 10,
                    "2": 20,
                    "3": 100,
                    "4": 300,
                    "5": 370
                },
                "common_issues": [...],
                "average_workflow_duration_ms": 250
            }

        Example:
            >>> summary = await client.rlhf.get_summary(
            ...     project_id="550e8400-...",
            ...     start_date="2025-01-01T00:00:00Z"
            ... )
        """
        params = {"project_id": project_id}

        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        return await self._client.execute("rlhf_get_summary", params)

    async def start_collection(
        self,
        project_id: str,
        session_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Start RLHF collection session

        Args:
            project_id: Project ID
            session_id: Session ID
            metadata: Optional session metadata

        Returns:
            {
                "session_id": "sess_123",
                "started_at": "...",
                "status": "active"
            }

        Example:
            >>> session = await client.rlhf.start_collection(
            ...     project_id="550e8400-...",
            ...     session_id="sess_123",
            ...     metadata={"user_id": "user_456", "environment": "production"}
            ... )
        """
        params = {
            "project_id": project_id,
            "session_id": session_id,
            "metadata": metadata or {}
        }

        return await self._client.execute("rlhf_start_collection", params)

    async def stop_collection(
        self,
        project_id: str,
        session_id: str
    ) -> Dict[str, Any]:
        """
        Stop RLHF collection session

        Args:
            project_id: Project ID
            session_id: Session ID

        Returns:
            {
                "session_id": "sess_123",
                "stopped_at": "...",
                "total_interactions": 15,
                "duration_seconds": 3600
            }

        Example:
            >>> result = await client.rlhf.stop_collection(
            ...     project_id="550e8400-...",
            ...     session_id="sess_123"
            ... )
        """
        params = {
            "project_id": project_id,
            "session_id": session_id
        }

        return await self._client.execute("rlhf_stop_collection", params)

    async def get_session_interactions(
        self,
        project_id: str,
        session_id: str,
        limit: int = 100,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Get interactions for a session

        Args:
            project_id: Project ID
            session_id: Session ID
            limit: Results per page
            offset: Number of results to skip

        Returns:
            {
                "interactions": [
                    {
                        "interaction_id": "...",
                        "interaction_type": "query",
                        "user_input": "...",
                        "agent_response": "...",
                        "feedback": {...},
                        "created_at": "..."
                    }
                ],
                "total": 15
            }

        Example:
            >>> interactions = await client.rlhf.get_session_interactions(
            ...     project_id="550e8400-...",
            ...     session_id="sess_123"
            ... )
        """
        params = {
            "project_id": project_id,
            "session_id": session_id,
            "limit": limit,
            "offset": offset
        }

        return await self._client.execute("rlhf_get_session_interactions", params)

    async def broadcast_event(
        self,
        project_id: str,
        event_type: str,
        event_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Broadcast RLHF event to subscribers

        Args:
            project_id: Project ID
            event_type: Event type
            event_data: Event data payload

        Returns:
            {
                "event_id": "uuid",
                "broadcasted_at": "...",
                "subscribers_notified": 5
            }

        Example:
            >>> event = await client.rlhf.broadcast_event(
            ...     project_id="550e8400-...",
            ...     event_type="feedback.received",
            ...     event_data={
            ...         "rating": 5,
            ...         "interaction_id": "int_456"
            ...     }
            ... )
        """
        params = {
            "project_id": project_id,
            "event_type": event_type,
            "event_data": event_data
        }

        return await self._client.execute("rlhf_broadcast_event", params)
