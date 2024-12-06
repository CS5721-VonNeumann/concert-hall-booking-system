from abc import ABC, abstractmethod
from users.middleware import get_current_user
from .models import Ticket, Show
from users.models import ShowProducer


class TicketSalesContext:
    def __init__(self, strategy):
        self.strategy = strategy

    def fetch_sales(self, show_name,slot_id):
        return self.strategy.fetch_ticket_sales(show_name,slot_id)

class TicketSalesStrategy(ABC):

    @abstractmethod
    def fetch_ticket_sales(self, show_id, slot_id):
        pass


class AdminTicketSalesStrategy(TicketSalesStrategy):

    def fetch_ticket_sales(self, show_name, slot_id=None):
        if slot_id:
            tickets = Ticket.objects.filter(
                show__name=show_name,   
                isCancelled=False,  
                show__slot_id=slot_id  )

        else:
            tickets = Ticket.objects.filter(
                show__name=show_name,   
                isCancelled=False)
        return tickets


class ShowProducerTicketSalesStrategy(TicketSalesStrategy):

    def fetch_ticket_sales(self, show_name,slot_id):
        user = get_current_user()
        user = ShowProducer.objects.get(user=user)
        tickets = Ticket.objects.filter(
                show__name=show_name,   
                isCancelled=False,  
                show__slot_id=slot_id,
                show__show_producer=user  )
        return tickets