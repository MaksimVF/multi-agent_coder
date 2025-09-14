
# Enhanced Event System for OpenHands

## Overview

The event system has been significantly enhanced to support complex, event-driven architectures with improved performance, reliability, and flexibility. These enhancements enable the OpenHands platform to handle more sophisticated workflows and agent coordination patterns.

## Key Improvements

### 1. Event Prioritization

Added `EventPriority` enum with levels:
- `LOW` - Background or non-critical events
- `NORMAL` - Standard priority events
- `HIGH` - Important events that need prompt handling
- `CRITICAL` - System-critical events that must be processed immediately

### 2. Middleware Support

Implemented a middleware framework that allows for:
- Event logging and monitoring
- Data validation and transformation
- Auditing and compliance tracking
- Custom processing pipelines

Included middleware implementations:
- `LoggingMiddleware` - Logs all events
- `ValidationMiddleware` - Validates event data against schemas
- `AuditMiddleware` - Adds audit information to events

### 3. Enhanced Event Validation

Added schema-based validation using Pydantic:
- `EventDataSchema` - Base schema for all events
- `TaskEventDataSchema` - Schema for task-related events
- `SubtaskEventDataSchema` - Schema for subtask events
- `ErrorEventDataSchema` - Schema for error events

### 4. Advanced Event Filtering

Enhanced event history querying with:
- Filtering by event type
- Filtering by priority level
- Filtering by source
- Time-based filtering
- Wildcard subscriptions

### 5. Performance Optimizations

- Asynchronous event processing with queue-based prioritization
- Configurable event history size limits
- Rate limiting for event sources
- Efficient subscriber notification

### 6. Enhanced Error Handling

Improved error handling with:
- Detailed error context preservation
- Error event generation with full context
- Prevention of infinite error loops
- Support for both async and sync error handlers

### 7. New Event Types

Added additional event types for more granular tracking:
- Agent lifecycle events (`AGENT_STATUS_CHANGED`)
- Memory events (`MEMORY_RECALLED`, `KNOWLEDGE_UPDATED`)
- Communication events (`MESSAGE_SENT`, `MESSAGE_RECEIVED`, etc.)
- System monitoring events (`SYSTEM_WARNING`)

## Usage Examples

### Creating Events with Prioritization and Validation

```python
from event_system import AgentEvent, EventType, EventPriority, TaskEventDataSchema

event = AgentEvent(
    event_type=EventType.TASK_CREATED,
    source="workflow_manager",
    data={
        "task_id": "task_123",
        "description": "Process user data",
        "priority": "high"
    },
    priority=EventPriority.HIGH,
    schema=TaskEventDataSchema
)
```

### Using Middleware

```python
from event_system import EventBus, LoggingMiddleware, AuditMiddleware

event_bus = EventBus(max_history=1000)
event_bus.add_middleware(LoggingMiddleware())
event_bus.add_middleware(AuditMiddleware())
```

### Advanced Event Querying

```python
# Get all high-priority events from a specific source
high_priority_events = event_bus.get_event_history(
    priority=EventPriority.HIGH,
    source="workflow_manager"
)

# Get recent task events
recent_tasks = event_bus.get_event_history(
    event_type=EventType.TASK_CREATED,
    limit=10
)
```

### Wildcard Subscriptions

```python
# Subscribe to all events
event_bus.subscribe("*", handle_all_events)
```

## Integration with Existing Systems

The enhanced event system maintains backward compatibility while providing new capabilities:

1. **Agent Workflow Integration**: The `AgentWorkflow` class now uses enhanced events with middleware and validation
2. **Memory Integration**: Events are stored in memory with enhanced metadata
3. **Error Handling**: Improved error tracking and recovery mechanisms

## Benefits

1. **Improved Reliability**: Better error handling and validation prevent system failures
2. **Enhanced Observability**: Middleware and logging provide better visibility into system operations
3. **Scalability**: Performance optimizations support higher event throughput
4. **Flexibility**: Advanced filtering and querying enable more sophisticated workflows
5. **Maintainability**: Schema validation ensures data consistency across the system

## Future Enhancements

1. **Event Persistence**: Long-term storage of events for auditing
2. **Event Replay**: Ability to replay events for system recovery
3. **Distributed Events**: Support for distributed event processing
4. **Security Features**: Event encryption and access control
5. **Analytics**: Real-time event analytics and monitoring

The enhanced event system provides a robust foundation for building complex, event-driven multi-agent systems with improved performance, reliability, and observability.
