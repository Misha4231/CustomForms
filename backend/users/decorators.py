from functools import wraps
from graphql import GraphQLError


def login_required(func):
    @wraps(func)
    def wrapper(cls, root, info, *args, **kwargs):
        user = info.context.user
        if not user or not user.is_authenticated:
            raise GraphQLError("Authentication required.")
        
        return func(cls, root, info, *args, **kwargs)

    return wrapper