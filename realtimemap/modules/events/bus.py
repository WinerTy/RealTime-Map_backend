import logging
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Callable, List, Optional

from modules.user.model import User

logger = logging.getLogger(__name__)


class EventType(str, Enum):
    MARK_CREATE = "create_mark"


@dataclass
class DomainEvent:
    event_type: EventType
    user: "User"
    source_type: Optional[str] = None
    source_id: Optional[int] = None
    metadata: Optional[Dict[str, str]] = None


class EventBus:
    def __init__(self):
        self._handlers: Dict[EventType, List[Callable]] = dict()

    def subscribe(self, event_type: EventType, callback: Callable):
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(callback)
        logger.info(f"Register callback {callback.__name__} for event {event_type}")

    async def publish(self, event: DomainEvent):
        handlers = self._handlers.get(event.event_type, [])

        for handler in handlers:
            try:
                await handler(event)
            except Exception as e:
                logger.error(f"Error in event {handler.__name__}: {e}", exc_info=True)


event_bus = EventBus()
