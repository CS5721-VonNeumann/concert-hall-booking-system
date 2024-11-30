from hall_manager.models import Seat
from ticket_manager.models import Ticket
from users.models import Customer

def return_available_seats(show_obj, seat_list: list):

    tickets = Ticket.objects.filter(
        show = show_obj,
        seat__seat_number__in = seat_list,
        isCancelled = False
    )

    if tickets.exists():
        return False

    seat_objs = Seat.objects.filter(
        seat_number__in=seat_list,
        hall=show_obj.hall
    )

    if seat_objs.exists():
        return seat_objs

    return False


def create_ticket(customer:Customer, show_obj, seat_objs, price_per_ticket):
    try:
        ticket_ids = []
        for seat in seat_objs:
            ticket = Ticket.objects.create(
                customer = customer,
                show = show_obj,
                seat = seat,
                price = price_per_ticket[seat.id]
            )
            ticket_ids.append(ticket.id)

        return ticket_ids
    except Exception as e:
        print(f"Something went wrong. Exception: {e}")
        return False