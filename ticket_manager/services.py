from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from show_manager.models import Show
from hall_manager.models import Seat
from ticket_manager.models import Ticket
from users.models import Customer

def return_available_seats(show_id: int, seat_list: list):
    show_obj = get_object_or_404(Show, id=show_id)

    tickets = Ticket.objects.filter(
        show = show_obj,
        seat__seat_number__in = seat_list
    )

    if tickets.exists():
        return False
    
    seat_objs = Seat.objects.filter(
        seat_number__in = seat_list, 
        hall = show_obj.hall
        )
    
    if seat_objs.exists():
        return seat_objs

    return False


def create_ticket(customer:Customer, show_id:int, seat_objs: QuerySet):
    try:
        show_obj = get_object_or_404(Show, id=show_id)
    except Exception as e:
        print(f"Something went wrong. Exception: {e}")
        return False
    else:
        ticket_ids =[]
        for seat in seat_objs:
            ticket = Ticket.objects.create(
                customer = customer,
                show = show_obj,
                seat = seat
            )
            ticket_ids.append(ticket.id)

        return ticket_ids