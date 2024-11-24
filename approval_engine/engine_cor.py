from show_manager.models import Show
from show_manager.showstatuses import PendingStatus
class ApprovalHandler:
    """
    Abstract handler for the approval process.
    """
    def __init__(self, next_handler=None):
        self.next_handler = next_handler


    def handle(self, show):
        if self.next_handler:
            return self.next_handler.handle(show)
        return True, ""  # Default success if no further handlers

class OverlappingShowValidationHandler(ApprovalHandler):
    """
    Handler to check for overlapping scheduled shows.
    """

    def handle(self, show):
        if Show.is_overlapping_show_exists(hall=show.hall, slot=show.slot):
            message = "Another show is already scheduled in the same hall and slot."
            return False, message
        return super().handle(show)

class CategorySupportValidationHandler(ApprovalHandler):
    """
    Handler to check if the hall supports the show's category.
    """
    def handle(self, show):
        if not show.hall.supports_category(category=show.category):
            message = "Validation failed: The hall does not support this show category."
            return False, message
        return super().handle(show)

class SlotSupportValidationHandler(ApprovalHandler):
    """
    Handler to check if the hall supports the show's slot.
    """
    def handle(self, show):
        if not show.hall.supports_slot(slot=show.slot):
            message = "Validation failed: The hall does not support this show slot."
            return False, message
        return super().handle(show)

class ApprovalEngine:
    """
    Engine for approving or rejecting show requests with CoR.
    """
    def __init__(self, show):
        self.show: Show = show
        # Assemble the chain of responsibility
        self.validation_chain = (
            OverlappingShowValidationHandler(
            CategorySupportValidationHandler(
            SlotSupportValidationHandler()
            ))
        )

    def handle_show_request(self):
        """
        Handles the show request by validating it through the chain.
        """
        try:
            if not isinstance(self.show.get_status_instance(), PendingStatus):
                print("Request not in pending status")
                return

            is_valid, message = self.validation_chain.handle(self.show)

            if is_valid:
                self.show.schedule()
            else:
                self.show.reject(message)
        except Exception as e:
            print(f"Error processing show request: {e}")
            self.show.reject("Error in validating request")
