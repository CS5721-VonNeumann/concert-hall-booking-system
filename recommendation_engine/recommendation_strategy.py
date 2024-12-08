from django.db.models import Count
from abc import ABC, abstractmethod

from show_manager.models import Show
from hall_manager.models import Hall
from ticket_manager.models import Ticket
from show_manager.serializers import ShowSerializer
from show_manager.showstatuses import ShowStatusEnum

class GlobalRecommendationContext:
    """
    Context class that manages the global recommendation strategy.

    Allows setting and getting a strategy and retrieving recommendations based on the given strategy.
    """
    _strategy = None

    @classmethod
    def set_strategy(self, strategy):
        self._strategy = strategy

    @classmethod
    def get_strategy(self):
        if self._strategy is None:
            raise ValueError("Global recommendation strategy is not set.")
        return self._strategy

    @classmethod
    def get_recommendations(self):
        strategy = self.get_strategy()
        return strategy.recommend()


class RecommendationStrategy(ABC):
    """
    Abstract base class for recommendation strategies.
    """

    @abstractmethod
    def recommend(self, **kwargs):
        pass

class LocationBasedRecommendation(RecommendationStrategy):
    def recommend(self, **kwargs):
        """
        Fetch shows from the database based on the hall's location.
        """
        location = kwargs.get('location')
        try:
            halls_in_location = Hall.objects.filter(venue__location=location)

            shows = Show.objects.filter(hall__in=halls_in_location, status=ShowStatusEnum.SCHEDULED.value)
            serialized_shows = ShowSerializer(shows, many=True).data

            return list(serialized_shows)

        except Exception as e:
            print(f"Error fetching recommendations: {e}")
            return []


class TrendingRecommendation(RecommendationStrategy):
    def recommend(self, **kwargs):
        """
        Fetch shows from the database based on ticket sales.
        """
        try:
            tickets = Ticket.objects.filter(isCancelled=False, status=ShowStatusEnum.SCHEDULED.value).values('show') \
                .annotate(total_tickets_sold=Count('id')) \
                .order_by('-total_tickets_sold')[:5]

            ticket_ids = [ticket['show'] for ticket in tickets]
            trending_shows = Show.objects.filter(id__in=ticket_ids) 
    
            serialized_shows = ShowSerializer(trending_shows, many=True).data

            return serialized_shows

        except Exception as e:
            print(f"Error fetching recommendations: {e}")
            return []
