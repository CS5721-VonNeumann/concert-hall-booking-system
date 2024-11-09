from abc import ABC, abstractmethod
from enum import Enum

class ShowStatusEnum(Enum):
    PENDING = 'PENDING',
    SCHEDULED = 'SCHEDULED',
    COMPLETED = 'COMPLETED',
    REJECTED = 'REJECTED',
    CANCELLED = 'CANCELLED'

class ShowStatus(ABC):
    """
    Abstract base class for show statuses. Enforces the implementation of
    the `get_status` in subclasses.
    """
    def __init__(self, show):
        self.show = show

    @abstractmethod
    def get_status(self):
        """Handle the current state logic."""
        pass


class PendingStatus(ShowStatus):
    def get_status(self):
        return ShowStatusEnum.PENDING

class ScheduledStatus(ShowStatus):
    def get_status(self):
        return ShowStatusEnum.SCHEDULED

class CompletedStatus(ShowStatus):
   def get_status(self):
        return ShowStatusEnum.COMPLETED

class RejectedStatus(ShowStatus):
    def get_status(self):
        return ShowStatusEnum.REJECTED

class CancelledStatus(ShowStatus):
    def get_status(self):
        return ShowStatusEnum.CANCELLED