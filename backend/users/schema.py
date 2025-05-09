import graphene
from graphene_django import DjangoObjectType
from graphene_file_upload.scalars import Upload
from graphql import GraphQLError
from django.contrib.auth.models import AnonymousUser

from .models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ["id", "email", "fullname", "avatar", "is_superuser"]
        

# update user mutation
class UserUpdateMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        fullname = graphene.String()
        avatar = Upload(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info: graphene.ResolveInfo, id, fullname, avatar, **kwargs):
        user: User | AnonymousUser = info.context.user
        if not user.is_authenticated or (id != user.id and not user.is_superuser): # random user can't update data
            raise GraphQLError("Permission denied")

        #assign new data
        user.fullname = fullname
        user.avatar = avatar # django ORM handles everything files related
        user.save()

        return UserUpdateMutation(user=user)
    
class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    profile = graphene.Field(UserType, id=graphene.Int())
    
    def resolve_me(root, info: graphene.ResolveInfo):
        return info.context.user
    
    def resolve_profile(root, info: graphene.ResolveInfo, id):
        return User.objects.get(pk=id)
    

class Mutation(graphene.ObjectType):
    update_user = UserUpdateMutation.Field()
