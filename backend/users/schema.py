import graphene
from graphene_django import DjangoObjectType
from .models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ["id", "email", "fullname", "avatar", "is_superuser"]
        
class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    
    def resolve_me(root, info: graphene.ResolveInfo):
        return info.context.user
    
schema = graphene.Schema(query=Query)