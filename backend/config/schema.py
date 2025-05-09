import graphene
from users.schema import Query as UsersQuery, Mutation as UsersMutation
from forms.schema import Query as FormsQuery, Mutation as FormsMutation


class Query(UsersQuery, FormsQuery, graphene.ObjectType):
    pass

class Mutation(UsersMutation, FormsMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)