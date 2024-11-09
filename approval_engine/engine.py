from show_manager.models import Show
from show_manager.showstatuses import ShowStatusEnum

class ApprovalEngine:
    """
    Engine for approving or rejecting show requests.
    """
    def __init__(self, show):
        self.show = show

    def validate_request(self):
        # check for overlapping scheduled shows
        overlapping_shows = Show.objects.filter(
            hall=self.show.hall,
            slot=self.show.slot,
            status=ShowStatusEnum.SCHEDULED.name
        ).exists()

        if overlapping_shows:
            print("Another show is already scheduled in the same hall and slot.")
            return False

        # check if the hall supports the requested category
        # if self.show.category not in self.show.hall.supported_categories:
        #     print("Validation failed: The hall does not support this show category.")
        #     return False

        # check if the hall supports the requested slot
        return True

    def process_request(self):
        if self.validate_request():
            self.show.approve()
        else:
            self.show.reject()
