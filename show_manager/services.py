from .models import Show
from users.models import ShowProducer
from hall_manager.models import Hall, Slot, Category
from approval_engine.tasks import handle_show_request
from approval_engine.engine_cor import ApprovalEngine

class ShowRequestService:
    @staticmethod
    def request_show(
        show_id: int,
        show_producer: ShowProducer,
        name: str,
        category: Category,
        has_intermission: bool,
        slot: Slot,
        hall: Hall
    ):
        """
        Creates a show request and triggers the asynchronous processing task.
        """
        try:
            if not show_id:
                show = Show.objects.create(
                    name=name,
                    category=category,
                    has_intermission=has_intermission,
                    slot=slot,
                    hall=hall,
                )
                show.attach(observer=show_producer)
            else:
                Show.objects.filter(id=show_id).update(
                    name=name, 
                    category=category,
                    has_intermission=has_intermission,
                    slot=slot,
                    hall=hall,
                )
                show = Show.objects.filter(id=show_id).first()

        except Exception as e:
            print(e)

        if not show_id:
            # synchronous: ApprovalEngine(show).handle_show_request()
            # asynchronous request to approval engine
            handle_show_request.delay(show.id)
            
        return show