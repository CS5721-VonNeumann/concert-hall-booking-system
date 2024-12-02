from payment_gateway.services import BillService, RefundService

class PaymentGatewayFacade:
    def __init__(self):
        self.bill_service = BillService()
        self.refund_service = RefundService()

    def get_ticket_bill_amount(self, customer_obj, seat_objs):
        price_per_ticket, bill_amount =  self.bill_service.get_ticket_bill_amount(customer_obj, seat_objs)
        return price_per_ticket, bill_amount
    
    def get_membership_bill_amount(self, membership_price):
        return self.bill_service.get_membership_bill_amount(membership_price)
    
    def get_ticket_refund(self, ticket_ids):
        return self.refund_service.get_ticket_refund(ticket_ids)
    
    def get_show_refund(self, show_id):
        return self.refund_service.get_show_refund(show_id)