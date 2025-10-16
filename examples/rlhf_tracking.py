"""
RLHF tracking example for ZeroDB MCP Python Client
"""

import asyncio
from zerodb_mcp import ZeroDBClient


async def main():
    client = ZeroDBClient(api_key="your_api_key_here")

    try:
        project_id = "your_project_id_here"
        session_id = "user_session_12345"

        # 1. Start RLHF collection session
        print("1. Starting RLHF collection session...")
        session = await client.rlhf.start_collection(
            project_id=project_id,
            session_id=session_id,
            metadata={
                "user_id": "user_789",
                "environment": "production"
            }
        )
        print(f"Session started: {session['session_id']}")

        # 2. Collect user-agent interaction
        print("\n2. Collecting interaction...")
        interaction = await client.rlhf.collect_interaction(
            session_id=session_id,
            project_id=project_id,
            interaction_type="query",
            user_input="How do I use quantum compression?",
            agent_response="Quantum compression uses quantum algorithms to...",
            context={
                "model": "gpt-4",
                "tokens_used": 150,
                "latency_ms": 850
            }
        )
        interaction_id = interaction["interaction_id"]
        print(f"Interaction recorded: {interaction_id}")

        # 3. Collect user feedback
        print("\n3. Collecting user feedback...")
        feedback = await client.rlhf.collect_agent_feedback(
            session_id=session_id,
            project_id=project_id,
            interaction_id=interaction_id,
            rating=5,
            feedback_text="Very clear and helpful explanation!",
            metadata={
                "helpful": True,
                "accurate": True,
                "complete": True
            }
        )
        print(f"Feedback collected: {feedback['feedback_id']}")

        # 4. Collect workflow feedback
        print("\n4. Collecting workflow feedback...")
        workflow_feedback = await client.rlhf.collect_workflow_feedback(
            session_id=session_id,
            project_id=project_id,
            workflow_id="quantum_compression_workflow",
            success=True,
            duration_ms=250,
            metadata={
                "compression_ratio": 12.0,
                "quality_preserved": 0.95
            }
        )
        print(f"Workflow feedback recorded")

        # 5. Report an error (if any)
        print("\n5. Reporting error (example)...")
        error = await client.rlhf.collect_error_report(
            session_id=session_id,
            project_id=project_id,
            error_type="ValidationError",
            error_message="Invalid vector dimensions",
            stack_trace="Traceback (most recent call last)...",
            context={
                "operation": "compress_vector",
                "input_dimensions": 2048
            }
        )
        print(f"Error reported: {error['error_id']}")

        # 6. Get session interactions
        print("\n6. Getting session interactions...")
        interactions = await client.rlhf.get_session_interactions(
            project_id=project_id,
            session_id=session_id
        )
        print(f"Total interactions in session: {interactions['total']}")
        for item in interactions['interactions']:
            print(f"- {item['interaction_type']}: {item['user_input'][:50]}...")

        # 7. Get RLHF status
        print("\n7. Getting RLHF status...")
        status = await client.rlhf.get_status(project_id)
        print(f"Active sessions: {status['active_sessions']}")
        print(f"Total interactions: {status['total_interactions']}")
        print(f"Average rating: {status['average_rating']:.2f}")

        # 8. Get RLHF summary
        print("\n8. Getting RLHF summary...")
        summary = await client.rlhf.get_summary(
            project_id=project_id,
            start_date="2025-01-01T00:00:00Z"
        )
        print(f"Total feedback: {summary['total_feedback']}")
        print(f"Rating distribution: {summary['rating_distribution']}")

        # 9. Stop collection session
        print("\n9. Stopping collection session...")
        stop_result = await client.rlhf.stop_collection(
            project_id=project_id,
            session_id=session_id
        )
        print(f"Session stopped. Duration: {stop_result['duration_seconds']}s")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
