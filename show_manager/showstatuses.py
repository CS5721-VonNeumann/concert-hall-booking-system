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

    def transition_to_scheduled(self):
        """Transition the status from 'Pending' to 'Scheduled'."""
        self.show.status = ShowStatusEnum.SCHEDULED.name
        self.show.save()
        print(f"Show status changed from {ShowStatusEnum.PENDING.name} to {ShowStatusEnum.SCHEDULED.name}")

    def transition_to_rejected(self):
        """Transition the status from 'Pending' to 'Rejected'."""
        self.show.status = ShowStatusEnum.REJECTED.name
        self.show.save()
        print(f"Show status changed from {ShowStatusEnum.PENDING.name} to {ShowStatusEnum.REJECTED.name}")

    def transition_to_cancelled(self):
        """Transition the status from 'Pending' to 'Cancelled'."""
        self.show.status = ShowStatusEnum.CANCELLED.name
        self.show.save()
        print(f"Show status changed from {ShowStatusEnum.PENDING.name} to {ShowStatusEnum.REJECTED.name}")



class ScheduledStatus(ShowStatus):
    def get_status(self):
        return ShowStatusEnum.SCHEDULED

    def transition_to_completed(self):
        """Transition the status from 'Scheduled' to 'Completed'."""
        self.show.status = ShowStatusEnum.COMPLETED.name
        self.show.save()
        print(f"Show status changed from {ShowStatusEnum.SCHEDULED.name} to {ShowStatusEnum.COMPLETED.name}")

class CompletedStatus(ShowStatus):
   def get_status(self):
        return ShowStatusEnum.COMPLETED

class RejectedStatus(ShowStatus):
    def get_status(self):
        return ShowStatusEnum.REJECTED

class CancelledStatus(ShowStatus):
    def get_status(self):
        return ShowStatusEnum.CANCELLED