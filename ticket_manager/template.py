from abc import ABC, abstractmethod
from hall_manager.models import TIMING_TO_TIME
from datetime import datetime
from ticket_manager.models import Ticket
from users.middleware import get_current_user
from .models import Customer

class TicketViewTemplate(ABC):
    def process_request(self, user):
        if not self.authenticate_user(user):
            raise PermissionError("User is not authorized to view tickets.")

        user = self.get_user(user)
        bookings = self.fetch_bookings(user)
        filtered_bookings = self.apply_filters(bookings)
        return filtered_bookings

    @abstractmethod
    def authenticate_user(self, user):
        """
        Must be implemented to define how a user is authenticated.
        """
        pass

    @abstractmethod
    def fetch_bookings(self, customer):
        """
        Must be implemented to fetch bookings for the given user.
        """
        pass

    @abstractmethod
    def get_user(self, user):
        """
        Override to customize how to retrieve the customer instance.
        """
        pass

    @abstractmethod
    def apply_filters(self, bookings):
        """
        Apply a chain of filters to bookings. Subclasses can override or add filters.
        """
        pass

class CustomerTicketView(TicketViewTemplate):
    def authenticate_user(self, user):
        return hasattr(user, 'customer')

    def fetch_bookings(self, customer):
        return Ticket.objects.filter(customer=customer)

    def apply_filters(self, bookings):
        upcoming_bookings = self.filter_upcoming(bookings)
        bookings = self.filter_cancelled(upcoming_bookings)
        return bookings

    def filter_upcoming(self, bookings):
        upcoming_tickets = []
        for ticket in bookings:
            show_time = ticket.getShowTimimg()
            show_date = ticket.getShowDate()
            show_datetime = datetime.combine(show_date, TIMING_TO_TIME[show_time])
            if datetime.now() < show_datetime:
                upcoming_tickets.append(ticket)
        return upcoming_tickets

    def filter_cancelled(self, bookings):
        return [ticket for ticket in bookings if not ticket.isCancelled]
    
    def get_user(self, user):
        return Customer.objects.get(user=get_current_user())