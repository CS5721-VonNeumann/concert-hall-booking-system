from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .recommendation_strategy import GlobalRecommendationContext, LocationBasedRecommendation, TrendingRecommendation

STRATEGY_MAP = {
    "location": LocationBasedRecommendation,
    "trending": TrendingRecommendation,
}

@api_view(['POST'])
def set_recommendation_strategy(request):
    """
    API to manage and fetch the global recommendation strategy.
    """
    strategy_name = request.data.get("strategy")

    if not strategy_name:
        return Response({"error": "Strategy name is required."}, status=status.HTTP_400_BAD_REQUEST)

    strategy_class = STRATEGY_MAP.get(strategy_name)

    if not strategy_class:
        return Response({"error": (
                        f"Invalid strategy name. Valid options are: "
                        f"{', '.join(STRATEGY_MAP.keys())}."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    # Set the global strategy
    GlobalRecommendationContext.set_strategy(strategy_class())
    
    return Response({"message": f"Global recommendation strategy set to '{strategy_name}'."},
            status=status.HTTP_200_OK)

@api_view(['GET'])
def get_recommendations(request):
    """
    View to fetch recommendations based on the chosen strategy.
    """
    try:
        # Fetch the global strategy
        strategy = GlobalRecommendationContext.get_strategy()
        location = request.GET.get('location', '').strip("'\" ")

        # Call the recommend method of the strategy
        if isinstance(strategy, LocationBasedRecommendation):
            recommendations = strategy.recommend(location)
        elif isinstance(strategy, TrendingRecommendation):
            recommendations = strategy.recommend()
        else:
            recommendations = strategy.recommend()

        return Response(
            {"message": "Recommendations fetched successfully.", "recommendations": recommendations},
            status=status.HTTP_200_OK,
        )
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)