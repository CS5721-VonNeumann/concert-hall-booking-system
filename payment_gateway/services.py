from membership.models import CustomerMembership
from payment_gateway.models import TransactionHistory, TransactionTypes
from ticket_manager.models import Ticket

class BillService:

    def get_ticket_bill_amount(self, customer_obj, seat_objs):
        try:
            prices = {seat.id : seat.get_seat_price() for seat in seat_objs}
            customer_membership_instance = (
                CustomerMembership.get_latest_valid_membership_instance(customer_obj)
                )
            
            discount_percentage = customer_membership_instance.get_ticket_discount_percentage()
            discounted_prices = {k: v * (1 - discount_percentage / 100) for k, v in prices.items()}
            return discounted_prices, sum(discounted_prices.values())
        except Exception as exc:
            return False, False

    def get_membership_bill_amount(self, membership_price):
        return membership_price

        
class RefundService:

    def get_ticket_refund(self, ticket_ids):
        try:
            tickets = Ticket.objects.filter(id__in = ticket_ids)
            customer_membership_instance = (
                CustomerMembership.get_latest_valid_membership_instance(
                    tickets.first().customer)
                )
            total_amount = sum(ticket.price for ticket in tickets)

            refund_percentage = customer_membership_instance.get_refund_percentage()
            refund_amount = total_amount * (refund_percentage / 100)

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