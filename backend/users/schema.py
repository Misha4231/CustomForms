import graphene
from graphene_django import DjangoObjectType
from .models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ["id", "email", "fullname", "avatar", "is_superuser"]
        
class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    profile = graphene.Field(UserType, id=graphene.Int())
    
    def resolve_me(root, info: graphene.ResolveInfo):
        return info.context.user
    
    def resolve_profile(root, info: graphene.ResolveInfo, id):
        return User.objects.get(pk=id)
    
schema = graphene.Schema(query=Query)