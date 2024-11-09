from .models import Show
from users.models import ShowProducer
from .models import ShowCategory, Slot
from hall_manager.models import Hall
from .showstatuses import ShowStatusEnum

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
        # from approval_engine.tasks import process_show_request
        # process_show_request.delay(show.id)
        return show