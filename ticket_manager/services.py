from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from membership.models import CustomerMembership
from hall_manager.models import Seat
from ticket_manager.models import Ticket
from users.models import Customer
from datetime import datetime, timedelta
from hall_manager.models import TIMING_TO_TIME

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

def is_ticket_cancellation_allowed(ticket_id,customer):
    current_membership = CustomerMembership.get_latest_valid_membership_instance(customer)
    cancel_time = current_membership.get_cancellation_time_policy()
    ticket = Ticket.objects.get(id=ticket_id)
    show_time = ticket.getShowTimimg()
    show_date = ticket.getShowDate()
    show_datetime = datetime.combine(show_date, TIMING_TO_TIME[show_time])
    allow_time = show_datetime - timedelta(hours=cancel_time)
    time = datetime.now() < allow_time
    return time