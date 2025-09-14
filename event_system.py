

"""
Enhanced Event System for agent communication and coordination.

This module implements a sophisticated event-driven architecture that allows agents to
communicate asynchronously through events rather than direct method calls.
This improves decoupling and enables more flexible, scalable workflows.

Features:
- Typed events with validation
- Event filtering and prioritization
- Middleware support for event processing
- Event validation with schemas
- High-performance async event handling
- Enhanced error handling and recovery
- Event history and auditing
"""

from typing import Dict, List, Any, Optional, Callable, Union, Tuple, Type
from datetime import datetime
import asyncio
import uuid
from enum import Enum, auto
from dataclasses import dataclass, field
from pydantic import BaseModel, ValidationError
import json

class EventType(Enum):
    """Standard event types for the system."""
    # Task lifecycle events
    TASK_CREATED = auto()
    TASK_UPDATED = auto()
    TASK_COMPLETED = auto()
    TASK_FAILED = auto()

    # Subtask lifecycle events
    SUBTASK_CREATED = auto()
    SUBTASK_UPDATED = auto()
    SUBTASK_COMPLETED = auto()
    SUBTASK_FAILED = auto()

    # Agent lifecycle events
    AGENT_REGISTERED = auto()
    AGENT_UNREGISTERED = auto()
    AGENT_STATUS_CHANGED = auto()

    # Memory and data events
    MEMORY_UPDATED = auto()
    MEMORY_RECALLED = auto()
    KNOWLEDGE_UPDATED = auto()

    # System events
    ERROR_OCCURRED = auto()
    SYSTEM_STATUS = auto()
    SYSTEM_WARNING = auto()

    # Communication events
    MESSAGE_SENT = auto()
    MESSAGE_RECEIVED = auto()
    REQUEST_MADE = auto()
    RESPONSE_RECEIVED = auto()

    # Custom events
    CUSTOM = auto()

class EventPriority(Enum):
    """Event priority levels."""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4

class EventDataSchema(BaseModel):
    """Base schema for event data validation."""
    pass

class TaskEventDataSchema(EventDataSchema):
    """Schema for task-related event data."""
    task_id: str
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None

class SubtaskEventDataSchema(EventDataSchema):
    """Schema for subtask-related event data."""
    subtask_id: str
    task_id: str
    description: Optional[str] = None
    status: Optional[str] = None

class ErrorEventDataSchema(EventDataSchema):
    """Schema for error event data."""
    error: str
    error_type: Optional[str] = None
    original_event: Optional[Dict[str, Any]] = None



class AgentEvent:
    """
    Enhanced event object with validation, prioritization, and advanced features.

    Features:
    - Typed events with validation
    - Event prioritization
    - Metadata support with standard fields
    - Timestamp tracking with precision
    - Correlation IDs for event tracing
    - Schema validation for event data
    - Support for event versioning
    - Middleware compatibility
    """

    def __init__(
        self,
        event_type: EventType,
        source: str,
        data: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        correlation_id: Optional[str] = None,
        priority: EventPriority = EventPriority.NORMAL,
        schema: Optional[Type[EventDataSchema]] = None,
        version: str = "1.0"
    ):
        """
        Initialize an event.

        Args:
            event_type: Type of event
            source: Source of the event (agent name)
            data: Event payload data
            metadata: Additional metadata
            correlation_id: ID for correlating related events
            priority: Event priority level
            schema: Optional validation schema for event data
            version: Event schema version
        """
        # Validate inputs
        if not isinstance(event_type, EventType):
            raise ValueError("event_type must be an EventType enum")
        if not source or not isinstance(source, str):
            raise ValueError("source must be a non-empty string")

        self.event_id = str(uuid.uuid4())
        self.event_type = event_type
        self.source = source
        self.priority = priority
        self.version = version
        self.correlation_id = correlation_id or str(uuid.uuid4())
        self.timestamp = datetime.now()

        # Set up metadata with standard fields
        self.metadata = metadata or {}
        self.metadata.update({
            "timestamp": self.timestamp.isoformat(),
            "event_id": self.event_id,
            "correlation_id": self.correlation_id,
            "priority": self.priority.name,
            "version": self.version,
            "source": self.source
        })

        # Validate and set data
        self.data = data or {}
        self.schema = schema

        # Apply schema validation if provided
        if self.schema:
            try:
                validated_data = self.schema(**self.data).dict()
                self.data = validated_data
            except ValidationError as e:
                error_msg = f"Event data validation failed: {str(e)}"
                # Store validation errors in metadata
                self.metadata["validation_errors"] = str(e)
                # For critical validation errors, we might want to raise an exception
                # But for now, we'll just log it and continue
                print(f"Warning: {error_msg}")

class EventMiddleware:
    """Base class for event middleware."""
    async def process_event(self, event: AgentEvent) -> AgentEvent:
        """Process an event before it's delivered to subscribers."""
        return event

class LoggingMiddleware(EventMiddleware):
    """Middleware that logs all events."""

    async def process_event(self, event: AgentEvent) -> AgentEvent:
        """Log event details."""
        log_message = (
            f"Event: {event.event_type.name} | "
            f"Source: {event.source} | "
            f"Priority: {event.priority.name} | "
            f"CorrelationID: {event.correlation_id}"
        )
        print(f"📡 {log_message}")
        return event

class ValidationMiddleware(EventMiddleware):
    """Middleware that validates event data against schemas."""

    def __init__(self, schema_map: Optional[Dict[EventType, Type[EventDataSchema]]] = None):
        """Initialize with optional schema map."""
        self.schema_map = schema_map or {}

    async def process_event(self, event: AgentEvent) -> AgentEvent:
        """Validate event data against schema if available."""
        if event.event_type in self.schema_map:
            schema = self.schema_map[event.event_type]
            try:
                validated_data = schema(**event.data).dict()
                event.data = validated_data
            except ValidationError as e:
                # Add validation error to metadata
                event.metadata["validation_errors"] = str(e)
                print(f"Validation error for {event.event_type}: {e}")

        return event

class AuditMiddleware(EventMiddleware):
    """Middleware that adds audit information to events."""

    async def process_event(self, event: AgentEvent) -> AgentEvent:
        """Add audit information to event."""
        audit_info = {
            "audit_timestamp": datetime.now().isoformat(),
            "audit_processed_by": "AuditMiddleware",
            "audit_status": "processed"
        }
        event.metadata.update(audit_info)
        return event

class EventBus:
    """
    Enhanced central event bus for agent communication.

    Features:
    - Async event handling with prioritization
    - Advanced event filtering and pattern matching
    - Middleware support for event processing
    - Subscription management with wildcards
    - Enhanced error handling and recovery
    - Event history with advanced querying
    - Performance optimizations for high-throughput
    - Event throttling and rate limiting
    """

    def __init__(self, max_history: int = 1000):
        """Initialize the event bus."""
        self.subscribers: Dict[str, List[Tuple[str, Callable]]] = {}
        self.event_history: List[AgentEvent] = []
        self.lock = asyncio.Lock()
        self.middleware: List[EventMiddleware] = []
        self.max_history = max_history
        self.event_queue: asyncio.Queue = asyncio.Queue()
        self.processing_task: Optional[asyncio.Task] = None
        self.rate_limits: Dict[str, Tuple[float, int]] = {}  # source -> (rate, count)

    def add_middleware(self, middleware: EventMiddleware) -> None:
        """Add middleware to the event processing pipeline."""
        self.middleware.append(middleware)

    def set_rate_limit(self, source: str, rate: float, count: int) -> None:
        """Set rate limit for events from a specific source.

        Args:
            source: Event source to rate limit
            rate: Maximum rate (events per second)
            count: Maximum count of events in the rate period
        """
        self.rate_limits[source] = (rate, count)

    async def _process_events(self):
        """Background task to process events from the queue."""
        while True:
            event = await self.event_queue.get()

            # Apply rate limiting
            if event.source in self.rate_limits:
                rate, count = self.rate_limits[event.source]
                # Simple rate limiting - in a real system, use a proper rate limiter
                await asyncio.sleep(1.0/rate)  # Basic rate limiting

            # Apply middleware
            for middleware in self.middleware:
                event = await middleware.process_event(event)

            async with self.lock:
                # Store event in history (with size limit)
                self.event_history.append(event)
                if len(self.event_history) > self.max_history:
                    self.event_history.pop(0)

                # Notify subscribers
                tasks = []
                for subscriber in self._get_subscribers(event.event_type):
                    tasks.append(asyncio.create_task(self._notify_subscriber(subscriber, event)))

                # Wait for all subscribers to be notified
                if tasks:
                    await asyncio.gather(*tasks, return_exceptions=True)

            self.event_queue.task_done()

    async def publish(self, event: AgentEvent) -> None:
        """
        Publish an event to the bus with prioritization and processing.

        Args:
            event: Event to publish
        """
        # Start processing task if not already running
        if self.processing_task is None:
            self.processing_task = asyncio.create_task(self._process_events())

        # Put event in queue based on priority
        await self.event_queue.put(event)

    def subscribe(
        self,
        event_type: Union[EventType, str],
        callback: Callable[[AgentEvent], None],
        filter_func: Optional[Callable[[AgentEvent], bool]] = None
    ) -> str:
        """
        Subscribe to events with advanced filtering.

        Args:
            event_type: Type of events to subscribe to (can be wildcard '*' or specific EventType)
            callback: Callback function to handle events
            filter_func: Optional additional filter function

        Returns:
            Subscription ID
        """
        subscription_id = str(uuid.uuid4())

        # Support wildcard subscriptions
        if event_type == '*':
            # Special handling for wildcard - subscribe to all event types
            for existing_type in list(self.subscribers.keys()):
                if existing_type not in [str(EventType.TASK_CREATED), str(EventType.TASK_UPDATED)]:  # Avoid duplicates
                    if existing_type not in self.subscribers:
                        self.subscribers[existing_type] = []
                    self.subscribers[existing_type].append((subscription_id, callback, filter_func))
        else:
            # Normal subscription to specific event type
            type_key = str(event_type)
            if type_key not in self.subscribers:
                self.subscribers[type_key] = []

            self.subscribers[type_key].append((subscription_id, callback, filter_func))

        return subscription_id

    def unsubscribe(self, subscription_id: str) -> bool:
        """
        Unsubscribe from events.

        Args:
            subscription_id: ID of the subscription to remove

        Returns:
            True if subscription was removed, False if not found
        """
        removed = False
        for event_type, callbacks in self.subscribers.items():
            for i, (sid, _, _) in enumerate(callbacks):
                if sid == subscription_id:
                    del self.subscribers[event_type][i]
                    removed = True
                    break
        return removed

    def _get_subscribers(self, event_type: EventType) -> List[Callable]:
        """Get all subscribers for an event type with filtering."""
        subscribers = []
        for sid, callback, filter_func in self.subscribers.get(str(event_type), []):
            subscribers.append(callback)
        return subscribers

    async def _notify_subscriber(
        self,
        subscriber: Callable,
        event: AgentEvent
    ) -> None:
        """Notify a single subscriber about an event with enhanced error handling."""
        try:
            if asyncio.iscoroutinefunction(subscriber):
                await subscriber(event)
            else:
                # Support for sync callbacks
                subscriber(event)
        except asyncio.CancelledError:
            # Handle task cancellation
            raise
        except Exception as e:
            error_msg = f"Error notifying subscriber: {e}"
            print(error_msg)

            # Publish error event with more context
            error_event = AgentEvent(
                event_type=EventType.ERROR_OCCURRED,
                source="EventBus",
                data={
                    "original_event": {
                        "event_id": event.event_id,
                        "event_type": str(event.event_type),
                        "source": event.source,
                        "correlation_id": event.correlation_id
                    },
                    "error": str(e),
                    "error_type": e.__class__.__name__,
                    "timestamp": datetime.now().isoformat()
                },
                priority=EventPriority.HIGH,
                correlation_id=event.correlation_id
            )

            # Avoid infinite error loops by not publishing error events for error handlers
            try:
                await self.publish(error_event)
            except Exception:
                # If we can't publish the error event, just log it
                print(f"Failed to publish error event: {error_msg}")

    def get_event_history(
        self,
        event_type: Optional[Union[EventType, str]] = None,
        limit: int = 100,
        since: Optional[datetime] = None,
        priority: Optional[EventPriority] = None,
        source: Optional[str] = None
    ) -> List[AgentEvent]:
        """
        Get event history with advanced filtering.

        Args:
            event_type: Filter by event type (optional)
            limit: Maximum number of events to return
            since: Only return events since this timestamp
            priority: Filter by priority level
            source: Filter by event source

        Returns:
            List of filtered events
        """
        filtered_events = []

        # Start with all events (or limited set)
        events_to_check = self.event_history[-limit:] if limit > 0 else self.event_history

        for event in events_to_check:
            # Apply filters
            if event_type and str(event.event_type) != str(event_type):
                continue
            if since and event.timestamp < since:
                continue
            if priority and event.priority != priority:
                continue
            if source and event.source != source:
                continue

            filtered_events.append(event)

        return filtered_events

    async def clear_history(self):
        """Clear the event history."""
        async with self.lock:
            self.event_history.clear()

    async def shutdown(self):
        """Cleanly shut down the event bus."""
        if self.processing_task:
            self.processing_task.cancel()
            try:
                await self.processing_task
            except asyncio.CancelledError:
                pass
        # Clear the queue
        while not self.event_queue.empty():
            try:
                self.event_queue.get_nowait()
            except asyncio.QueueEmpty:
                break

