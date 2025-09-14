

"""
Event System for agent communication and coordination.

This module implements an event-driven architecture that allows agents to
communicate asynchronously through events rather than direct method calls.
This improves decoupling and enables more flexible workflows.
"""

from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
import asyncio
import uuid
from enum import Enum, auto

class EventType(Enum):
    """Standard event types for the system."""
    TASK_CREATED = auto()
    TASK_UPDATED = auto()
    TASK_COMPLETED = auto()
    TASK_FAILED = auto()
    SUBTASK_CREATED = auto()
    SUBTASK_UPDATED = auto()
    SUBTASK_COMPLETED = auto()
    SUBTASK_FAILED = auto()
    AGENT_REGISTERED = auto()
    AGENT_UNREGISTERED = auto()
    MEMORY_UPDATED = auto()
    ERROR_OCCURRED = auto()
    SYSTEM_STATUS = auto()
    CUSTOM = auto()

class AgentEvent:
    """
    Event object that contains all information about an event.

    Features:
    - Typed events with validation
    - Metadata support
    - Timestamp tracking
    - Correlation IDs for event tracing
    """

    def __init__(
        self,
        event_type: EventType,
        source: str,
        data: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        correlation_id: Optional[str] = None
    ):
        """
        Initialize an event.

        Args:
            event_type: Type of event
            source: Source of the event (agent name)
            data: Event payload data
            metadata: Additional metadata
            correlation_id: ID for correlating related events
        """
        self.event_id = str(uuid.uuid4())
        self.event_type = event_type
        self.source = source
        self.data = data or {}
        self.metadata = metadata or {}
        self.timestamp = datetime.now()
        self.correlation_id = correlation_id or str(uuid.uuid4())

        # Add standard metadata
        self.metadata.update({
            "timestamp": self.timestamp.isoformat(),
            "event_id": self.event_id,
            "correlation_id": self.correlation_id
        })

class EventBus:
    """
    Central event bus for agent communication.

    Features:
    - Async event handling
    - Event filtering
    - Subscription management
    - Error handling
    - Event history
    """

    def __init__(self):
        """Initialize the event bus."""
        self.subscribers: Dict[str, List[Callable]] = {}
        self.event_history: List[AgentEvent] = []
        self.lock = asyncio.Lock()

    async def publish(self, event: AgentEvent) -> None:
        """
        Publish an event to the bus.

        Args:
            event: Event to publish
        """
        async with self.lock:
            # Store event in history
            self.event_history.append(event)

            # Notify subscribers
            tasks = []
            for subscriber in self._get_subscribers(event.event_type):
                tasks.append(asyncio.create_task(self._notify_subscriber(subscriber, event)))

            # Wait for all subscribers to be notified
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)

    def subscribe(
        self,
        event_type: EventType,
        callback: Callable[[AgentEvent], None]
    ) -> str:
        """
        Subscribe to events of a specific type.

        Args:
            event_type: Type of events to subscribe to
            callback: Callback function to handle events

        Returns:
            Subscription ID
        """
        subscription_id = str(uuid.uuid4())
        if str(event_type) not in self.subscribers:
            self.subscribers[str(event_type)] = []

        self.subscribers[str(event_type)].append((subscription_id, callback))
        return subscription_id

    def unsubscribe(self, subscription_id: str) -> bool:
        """
        Unsubscribe from events.

        Args:
            subscription_id: ID of the subscription to remove

        Returns:
            True if subscription was removed, False if not found
        """
        for event_type, callbacks in self.subscribers.items():
            for i, (sid, _) in enumerate(callbacks):
                if sid == subscription_id:
                    del self.subscribers[event_type][i]
                    return True
        return False

    def _get_subscribers(self, event_type: EventType) -> List[Callable]:
        """Get all subscribers for an event type."""
        return [callback for _, callback in self.subscribers.get(str(event_type), [])]

    async def _notify_subscriber(
        self,
        subscriber: Callable,
        event: AgentEvent
    ) -> None:
        """Notify a single subscriber about an event."""
        try:
            await subscriber(event)
        except Exception as e:
            print(f"Error notifying subscriber: {e}")
            # Publish error event
            error_event = AgentEvent(
                event_type=EventType.ERROR_OCCURRED,
                source="EventBus",
                data={
                    "original_event": event,
                    "error": str(e)
                },
                correlation_id=event.correlation_id
            )
            await self.publish(error_event)

    def get_event_history(
        self,
        event_type: Optional[EventType] = None,
        limit: int = 100
    ) -> List[AgentEvent]:
        """
        Get event history with optional filtering.

        Args:
            event_type: Filter by event type (optional)
            limit: Maximum number of events to return

        Returns:
            List of events
        """
        if event_type:
            return [
                event for event in self.event_history[-limit:]
                if event.event_type == event_type
            ]
        return self.event_history[-limit:]

