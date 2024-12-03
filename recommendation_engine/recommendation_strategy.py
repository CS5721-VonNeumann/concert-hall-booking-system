from abc import ABC, abstractmethod
from show_manager.models import Show
from hall_manager.models import Hall
from show_manager.serializers import ShowSerializer

class GlobalRecommendationContext:
    """
    A context for managing a single global recommendation strategy.
    """

    _strategy = None  # Holds the global strategy instance

    @classmethod
    def set_strategy(self, strategy):
        """
        Set the global recommendation strategy.
        """
        self._strategy = strategy
        print(f"Global strategy set to {self._strategy.__class__.__name__}.")

    @classmethod
    def get_strategy(self):
        """
        Get the current global recommendation strategy.
        """
        if self._strategy is None:
            raise ValueError("Global recommendation strategy is not set.")
        return self._strategy

    @classmethod
    def get_recommendations(self):
        """
        Fetch recommendations using the global strategy.
        """
        strategy = self.get_strategy()
        print(f"Fetching recommendations using {strategy.__class__.__name__}.")
        return strategy.recommend()


class RecommendationStrategy(ABC):
    """
    Abstract base class for recommendation strategies.
    """

    @abstractmethod
    def recommend(self):
        pass


# Concrete recommendation strategies
class LocationBasedRecommendation(RecommendationStrategy):
    def recommend(self, location):
        """
        Fetch shows from the database based on the hall's location.
        """
        try:
            # Fetch halls associated with the given location
            halls_in_location = Hall.objects.filter(venue__location=location)

            # Fetch shows associated with these halls
            shows = Show.objects.filter(hall__in=halls_in_location, status="SCHEDULED")
            serialized_shows = ShowSerializer(shows, many=True)

            return list(serialized_shows.data)

        except Exception as e:
            print(f"Error fetching recommendations: {e}")
            return []


# based on show sales
class TrendingRecommendation(RecommendationStrategy):
    def recommend(self):
        return ["Show X", "Show Y", "Show Z"]
