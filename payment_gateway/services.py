from membership.models import CustomerMembership
from payment_gateway.models import TransactionHistory, TransactionTypes
from ticket_manager.models import Ticket

class BillService:

    def get_ticket_bill_amount(self, customer_obj, seat_objs):
        try:
            total_amount = sum(seat.get_seat_price() for seat in seat_objs)
            customer_membership = CustomerMembership.get_latest_valid_membership(customer_obj)
            discount_percentage = (customer_membership.
                                get_membership_type_class().
                                get_ticket_discount_percentage()
                                )
            ticket_bill_amount = total_amount * (1 - discount_percentage / 100)
            return ticket_bill_amount
        except Exception as exc:
            return False

    def get_membership_bill_amount(self, membership_price):
        return membership_price

        
class RefundService:

    def get_ticket_refund(self, ticket_ids):
        try:
            tickets = Ticket.objects.filter(id__in = ticket_ids)
            customer_membership = CustomerMembership.get_latest_valid_membership(tickets.first().customer)

            total_amount = sum(ticket.seat.get_seat_price() for ticket in tickets)
            discount_percentage = (customer_membership.
                                    get_membership_type_class().
                                    get_ticket_discount_percentage()
                                    )
            ticket_bill_amount = total_amount * (1 - discount_percentage / 100)

            refund_percentage = (customer_membership.
                                    get_membership_type_class().
                                    get_refund_percentage()
                                    )
            refund_amount = ticket_bill_amount * (refund_percentage / 100)

            return refund_amount
        except Exception as exc:
            return False

    def get_show_refund():
        pass



def create_transaction(
        customer,
        transaction_type,
        amount
):
    if isinstance(transaction_type, TransactionTypes):
        transaction_type = transaction_type.value
    else:
        raise ValueError(f"Expected an instance of {TransactionTypes.__name__}, but got {type(transaction_type)}")
    
    TransactionHistory.objects.create(
        customer=customer,
        transaction_type=transaction_type,
        amount=amount
    )