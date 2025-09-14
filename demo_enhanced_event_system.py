

"""
Demo script showing the enhanced event system capabilities.

This script demonstrates:
1. Event prioritization
2. Middleware usage
3. Event validation with schemas
4. Advanced filtering and querying
5. Rate limiting
6. Error handling improvements
"""

import os
import json
import asyncio
from typing import Dict, Any, List

# Import enhanced event system components
from event_system import (
    EventBus,
    EventType,
    AgentEvent,
    EventPriority,
    EventDataSchema,
    TaskEventDataSchema,
    ErrorEventDataSchema,
    LoggingMiddleware,
    ValidationMiddleware,
    AuditMiddleware
)

async def demo_enhanced_event_system():
    """Demonstrate the enhanced event system capabilities."""
    print("\n🚀 Demo: Enhanced Event System")

    # Create enhanced event bus with middleware
    event_bus = EventBus(max_history=500)

    # Add middleware
    event_bus.add_middleware(LoggingMiddleware())
    event_bus.add_middleware(AuditMiddleware())

    # Add validation middleware with schemas
    validation_middleware = ValidationMiddleware({
        EventType.TASK_CREATED: TaskEventDataSchema,
        EventType.TASK_UPDATED: TaskEventDataSchema,
        EventType.ERROR_OCCURRED: ErrorEventDataSchema
    })
    event_bus.add_middleware(validation_middleware)

    # Define event handlers with different priorities
    async def handle_high_priority_event(event: AgentEvent):
        print(f"🔥 High Priority Handler: Processing {event.event_type.name} - {event.data}")

    async def handle_normal_event(event: AgentEvent):
        print(f"📋 Normal Handler: Processing {event.event_type.name} - {event.data}")

    async def handle_error_event(event: AgentEvent):
        print(f"⚠️ Error Handler: {event.data.get('error')}")

    # Subscribe to events with different priorities
    sub1 = event_bus.subscribe(EventType.TASK_CREATED, handle_high_priority_event)
    sub2 = event_bus.subscribe(EventType.TASK_UPDATED, handle_normal_event)
    sub3 = event_bus.subscribe(EventType.ERROR_OCCURRED, handle_error_event)

    # Set rate limit for demo source
    event_bus.set_rate_limit("demo_system", rate=5.0, count=10)  # Max 5 events per second

    # Publish events with different priorities and schemas
    print("\n--- Publishing Events with Different Priorities ---")

    # Create a high priority event with schema validation
    task_created_event = AgentEvent(
        event_type=EventType.TASK_CREATED,
        source="demo_system",
        data={
            "task_id": "enhanced_task_001",
            "description": "Enhanced task with validation",
            "status": "created",
            "priority": "high"
        },
        priority=EventPriority.HIGH,
        schema=TaskEventDataSchema
    )

    await event_bus.publish(task_created_event)

    # Create a normal priority event
    task_updated_event = AgentEvent(
        event_type=EventType.TASK_UPDATED,
        source="demo_system",
        data={
            "task_id": "enhanced_task_001",
            "status": "running"
        },
        priority=EventPriority.NORMAL,
        schema=TaskEventDataSchema
    )

    await event_bus.publish(task_updated_event)

    # Create an event with invalid data to test validation
    invalid_event = AgentEvent(
        event_type=EventType.TASK_CREATED,
        source="demo_system",
        data={
            # Missing required task_id field
            "description": "Invalid task without ID",
            "status": "invalid"
        },
        priority=EventPriority.NORMAL,
        schema=TaskEventDataSchema
    )

    await event_bus.publish(invalid_event)

    # Create an error event
    error_event = AgentEvent(
        event_type=EventType.ERROR_OCCURRED,
        source="demo_system",
        data={
            "error": "Demo validation error",
            "error_type": "ValidationError",
            "original_event": {"event_id": "invalid_001"}
        },
        priority=EventPriority.HIGH,
        schema=ErrorEventDataSchema
    )

    await event_bus.publish(error_event)

    # Demonstrate advanced event history querying
    print("\n--- Advanced Event History Querying ---")

    # Get all events
    all_events = event_bus.get_event_history(limit=10)
    print(f"Total events in history: {len(all_events)}")

    # Get only high priority events
    high_priority_events = event_bus.get_event_history(priority=EventPriority.HIGH)
    print(f"High priority events: {len(high_priority_events)}")

    # Get events from specific source
    demo_events = event_bus.get_event_history(source="demo_system")
    print(f"Events from demo_system: {len(demo_events)}")

    # Get events of specific type
    task_events = event_bus.get_event_history(event_type=EventType.TASK_CREATED)
    print(f"TASK_CREATED events: {len(task_events)}")

    # Demonstrate wildcard subscription
    async def handle_all_events(event: AgentEvent):
        print(f"🌐 Wildcard Handler: {event.event_type.name} from {event.source}")

    wildcard_sub = event_bus.subscribe("*", handle_all_events)

    # Publish another event to test wildcard
    test_event = AgentEvent(
        event_type=EventType.SUBTASK_CREATED,
        source="demo_system",
        data={
            "subtask_id": "subtask_001",
            "task_id": "enhanced_task_001",
            "description": "Test subtask"
        }
    )

    await event_bus.publish(test_event)

    # Clean up
    await event_bus.shutdown()

    print("\n✅ Enhanced Event System Demo Completed!")

async def main():
    """Run the enhanced event system demo."""
    print("🚀 Running Enhanced Event System Demo...")
    await demo_enhanced_event_system()

if __name__ == "__main__":
    asyncio.run(main())

