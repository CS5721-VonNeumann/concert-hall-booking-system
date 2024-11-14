from show_manager.models import Show
from show_manager.showstatuses import ShowStatusEnum
from hall_manager.models import Slot, Category, Hall
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict

class ApprovalEngine:
    """
    Engine for approving or rejecting show requests.
    """
    def __init__(self, show):
        self.show: Show = show

    def validate_show_request(self):
        try:
            hall= self.show.hall
            slot=self.show.slot
            category = self.show.category
            
            # check for overlapping scheduled shows
            if Show.is_overlapping_show_exists(hall= self.show.hall, slot= self.show.slot):
                message = "Another show is already scheduled in the same hall and slot."
                print(message)
                return False, message

            if not hall.supports_category(category=category):
                message = "Validation failed: The hall does not support this show category."
                print(message)
                return False, message

            if not hall.supports_slot(slot=slot):
                message = "Validation failed: The hall does not support this show slot."
                print(message)
                return False, message
            
            return True, ""
        except Exception as e:
            print(e)
            return False, "Error in validating request"

    def handle_show_request(self):
        is_valid, message = self.validate_show_request()
        if is_valid:
            self.show.schedule()
        else:
            self.show.reject(message)
