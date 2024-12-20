from django.db.models import Count
from abc import ABC, abstractmethod

from show_manager.models import Show
from hall_manager.models import Hall
from ticket_manager.models import Ticket
from show_manager.serializers import ShowSerializer

class GlobalRecommendationContext:
    _strategy = None  # Holds the global strategy instance

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
    def recommend(self):
        pass

class LocationBasedRecommendation(RecommendationStrategy):
    def recommend(self, location):
        """
        Fetch shows from the database based on the hall's location.
        """
        try:
            halls_in_location = Hall.objects.filter(venue__location=location)

            shows = Show.objects.filter(hall__in=halls_in_location, status="SCHEDULED")
            serialized_shows = ShowSerializer(shows, many=True).data

            return list(serialized_shows)

        except Exception as e:
            print(f"Error fetching recommendations: {e}")
            return []


class TrendingRecommendation(RecommendationStrategy):
    def recommend(self):
        """
        Fetch shows from the database based on ticket sales.
        """
        try:
            tickets = Ticket.objects.filter(isCancelled=False).values('show') \
                .annotate(total_tickets_sold=Count('id')) \
                .order_by('-total_tickets_sold')[:5]

            ticket_ids = [ticket['show'] for ticket in tickets]
            trending_shows = Show.objects.filter(id__in=ticket_ids) 
    
            serialized_shows = ShowSerializer(trending_shows, many=True).data

            return serialized_shows

        except Exception as e:
            print(f"Error fetching recommendations: {e}")
            return []
