import graphene
from graphene_django import DjangoObjectType
from graphene_django import DjangoListField
from .models import Form, Section, Content, Question, QuestionOption, Answer
from users.models import User

class FormType(DjangoObjectType):
    class Meta:
        model = Form
        fields = ('id', 'title', 'description', 'owner')

class SectionType(DjangoObjectType):
    class Meta:
        model = Section
        fields = ('id', 'title', 'type')

class ContentType(DjangoObjectType):
    class Meta:
        model = Content
        fields = ('id', 'type', 'text', 'image', 'video')
        
class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = ('id', 'answer_type', 'is_required', 'min_range', 'max_range')
        
class QuestionOptionType(DjangoObjectType):
    class Meta:
        model = QuestionOption
        fields = ('id', 'text')
        
class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer
        fields = ('id', 'submitted_at', 'short_text', 'long_text', 'range_value', 'date_value')


class FormCreateMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String()
        owner = graphene.Int()
    
    form = graphene.Field(FormType)
    
    @classmethod
    def mutate(cls, root, info, title, description, owner):
        user = User.objects.get(pk=owner)
        form = Form(title=title, description=description, owner=user)
        form.save()
        return FormCreateMutation(form=form)
        
class FormUpdateMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        title = graphene.String(required=True)
        description = graphene.String()
    
    form = graphene.Field(FormType)
    
    @classmethod
    def mutate(cls, root, info, id, title, description=None):
        form = Form.objects.get(pk=id)
        form.title = title
        if description:
            form.description = description
        form.save()
        
        return FormUpdateMutation(form=form)
        

class Query(graphene.ObjectType):
    all_forms = graphene.Field(FormType, id=graphene.Int())
    all_sections = graphene.List(SectionType, id=graphene.Int())
    
    def resolve_all_forms(root, info, id):
        return Form.objects.get(pk=id)

    def resolve_all_sections(root, info, id):
        return Section.objects.filter(form=id)
    
class Mutation(graphene.ObjectType):
    create_form = FormCreateMutation.Field()
    update_form = FormUpdateMutation.Field()
