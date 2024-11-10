from .models import Show
from users.models import ShowProducer
from .models import ShowCategory, Slot
from hall_manager.models import Hall
from .showstatuses import ShowStatusEnum
from approval_engine.tasks import process_show_request
from approval_engine.engine import ApprovalEngine

class ShowRequestService:
    @staticmethod
    def request_show(
        show_producer: ShowProducer,
        name: str,
        category: ShowCategory,
        has_intermission: bool,
        slot: Slot,
        hall: Hall
    ):
        """
        Creates a show request and triggers the asynchronous processing task.
        """
        try:
            show = Show.objects.create(
                show_producer=show_producer,
                name=name,
                category=category,
                has_intermission=has_intermission,
                slot=slot,
                hall=hall,
            )
        except Exception as e:
            print(e)

        # asynchronous request to approval engine
        process_show_request.delay(show.id)

        return show