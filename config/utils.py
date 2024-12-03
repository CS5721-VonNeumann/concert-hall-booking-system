from drf_yasg import openapi

def get_query_param_schema(name, required=True, description=None):
    """
    Function to generate query param option in swagger docs
    """
    return openapi.Parameter(
        name = name,
        in_ = openapi.IN_QUERY,
        type = openapi.TYPE_STRING,
        required = required,
        description = description
    )