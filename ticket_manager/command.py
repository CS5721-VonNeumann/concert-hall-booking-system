from .models import Ticket
from django.core.exceptions import ValidationError
from django.db import models
from payment_gateway.services import RefundService

class Command():
    def execute(self):
        pass

class CancelTicketCommand(Command):
    def __init__(self, ticket_ids, customer):
        self.ticket_ids = ticket_ids
        self.customer = customer

    def execute(self):
        # Fetch the ticket from the database
        tickets=[]
        for t_id in self.ticket_ids:
            ticket = Ticket.objects.get(id=t_id, customer=self.customer)
            # Cancel the ticket
            ticket.cancel()
            tickets.append(ticket)
        return tickets

class RefundCommand(Command):
    def __init__(self, customer, ticket_ids):
        self.customer = customer
        self.ticket_ids = ticket_ids

    def execute(self):
        try:
            # Utilize the RefundService for calculating refund
            refund_service = RefundService()
            refund_amount=0
            for ticket_id in self.ticket_ids:
                refund = refund_service.get_ticket_refund(self.ticket_ids)
                if refund!=None:
                    refund_amount+=refund
                if refund_amount is False:
                    raise Exception("Refund calculation failed.")
            # Mock actual refund processing
            self.process_refund(refund_amount)
            return f"Refund of {refund_amount} successfully processed for tickets {self.ticket_ids}."
        except Exception as e:
            raise Exception(f"Refund processing failed: {str(e)}")

    def process_refund(self, amount):
        print(f"Processed refund of amount: {amount}")


class LoyaltyDeductionCommand(Command):
    def __init__(self, customer, ticket_ids):
        self.customer = customer
        self.ticket_ids = ticket_ids

    def execute(self):
        pass

