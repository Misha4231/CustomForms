import graphene
from graphene_django import DjangoObjectType
from graphene_django import DjangoListField
from graphql import GraphQLError

from .models import Form, Section, Content, Question, QuestionOption, Answer
from users.models import User
from .types import *


class FormCreateMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String(required=False)
    
    form = graphene.Field(FormType)
    
    @classmethod
    def mutate(cls, root, info, title, description = ''):
        if not info.context.user.is_authenticated:
            raise GraphQLError("not authenticated")
        
        form = Form(title=title, description=description, owner=info.context.user)
        form.save()
        return FormCreateMutation(form=form)
        
class FormUpdateMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        title = graphene.String()
        description = graphene.String()
    
    form = graphene.Field(FormType)
    
    @classmethod
    def mutate(cls, root, info, id, title=None, description=None):
        form = Form.objects.get(pk=id)
        if title != None: # can be empty string
            form.title = title
        if description != None:
            form.description = description
        form.save()
        
        return FormUpdateMutation(form=form)
        

class Query(graphene.ObjectType):
    all_user_forms = graphene.List(FormType, userId=graphene.Int(required=True))
    form = graphene.Field(FormType, id=graphene.Int(required=True))
    sections_by_form = graphene.List(SectionType, form_id=graphene.ID(required=True))
    section_options = graphene.List(QuestionOptionType, section_id=graphene.ID(required=True))

    def resolve_all_user_forms(root, info, userId):
        return Form.objects.filter(owner__id=userId).order_by('-pk')

    def resolve_form(root, info, id):
        return Form.objects.get(pk=id)

    def resolve_sections_by_form(root, info, form_id):
        return Section.objects.filter(form__id=form_id)
    
    def resolve_section_options(root, info, section_id):
        return QuestionOption.objects.select_related('question__section').filter(question__section__id=section_id)
    
class Mutation(graphene.ObjectType):
    create_form = FormCreateMutation.Field()
    update_form = FormUpdateMutation.Field()
