import graphene
from graphene_django import DjangoObjectType
from graphene_django import DjangoListField
from graphql import GraphQLError
from django.db.models import Max, F

from .models import Form, Section, Content, Question, QuestionOption, Answer
from users.models import User
from .types import *
from .decorstors import form_owner, form_owner_section_id

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
        
class SectionCreateMutation(graphene.Mutation):
    class Arguments:
        form_id = graphene.ID()
        type = graphene.String()
        order = graphene.Int()

    section = graphene.Field(SectionType)

    @classmethod
    @form_owner
    def mutate(cls, root, info, form, type = 'question', order = 0):
        sections = Section.objects.filter(form=form)

        max_order = sections.aggregate(Max('order'))['order__max'] or 0 # get the maximum order value from sections
        if order > max_order + 1: # if order argument is grater then the maximum possible order
            order = max_order + 1
    
        # increment order of sections at or after the desired insert position
        sections.filter(order__gte=order).update(order=F('order') + 1)

        # create new section
        section = Section.objects.create(
            title='',
            form=form,
            type='question' if type == 'question' else 'content',
            order=order
        )

        if type == 'question':
            Question.objects.create(section=section, answer_type='short')
        else:
            Content.objects.create(section=section, type=type)

        return SectionCreateMutation(section)

class SectionRemoveMutation(graphene.Mutation):
    class Arguments:
        section_id = graphene.ID()

    ok = graphene.Boolean()

    @classmethod
    @form_owner_section_id
    def mutate(cls, root, info, form: Form, section: Section):
        Section.objects.filter(form=form, order__gt=section.order).update(order=F('order') - 1)

        section.delete()
        return SectionRemoveMutation(True)
        

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
        return Section.objects.filter(form__id=form_id).order_by('order')
    
    def resolve_section_options(root, info, section_id):
        return QuestionOption.objects.select_related('question__section').filter(question__section__id=section_id)
    
class Mutation(graphene.ObjectType):
    create_form = FormCreateMutation.Field()
    update_form = FormUpdateMutation.Field()
    add_section = SectionCreateMutation.Field()
    remove_section = SectionRemoveMutation.Field()