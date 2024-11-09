from show_manager.models import Show

class ApprovalEngine:
    """
    Engine for approving or rejecting show requests.
    """
    def __init__(self, show):
        self.show = show

    def validate_request(self):
        # Example validation logic: check for overlapping scheduled shows
        if Show.objects.filter(hall_name=self.show.hall_name, date_time=self.show.date_time, status='Scheduled').exists():
            return False
        return True

    def process_request(self):
        if self.validate_request():
            self.show.approve()
        else:
            self.show.reject()
