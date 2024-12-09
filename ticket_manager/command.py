from .models import Ticket
from django.core.exceptions import ValidationError
from django.db import models
from payment_gateway.services import RefundService
from shared.command import Command

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
            refund = refund_service.get_ticket_refund(self.ticket_ids)
            if refund!=None:
                refund_amount+=refund
            if refund_amount is False:
                raise Exception("Refund calculation failed.")
            # Mock actual refund processing
            return f"Refund Initiated."
        except Exception as e:
            raise Exception(f"Refund processing failed: {str(e)}")

class CommandInvoker:
    def __init__(self, cancel_command, refund_command):
        self.cancel_command = cancel_command
        self.refund_command = refund_command
        
    def command_execute(self):
        cancel_message = self.cancel_command.execute()
        refund_message = self.refund_command.execute()
        return cancel_message, refund_message
